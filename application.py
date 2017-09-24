from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_database_setup import Base, User, BookCategory, Book


# New imports for creating anti-forgery state token
from flask import session as login_session
import random
import string


# New Imports for GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Book Catalog Application"

engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Function
def createUser(login_session):
    newUser = User(name=login_session['username'],email=login_session
        ['email'],picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user =  session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCOONECT -  Revoke a current user's token and reset their login session.
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON endpoint for books from one category
# Making an API endpoint for books from one category
@app.route('/cataloghome/<int:bookcategory_id>/books/JSON/')
def catalogJSON(bookcategory_id):
    bookcjkategory = session.query(
        BookCategory).filter_by(id=bookcategory_id).one()
    items = session.query(Book).filter_by(
        bookcategory_id=bookcategory_id).all()
    return jsonify(Books=[i.serialize for i in items])

# JSON endpoint for a certain book in a category
@app.route('/cataloghome/<int:bookcategory_id>/books/<int:id>/JSON/')
def bookJSON(bookcategory_id, id):
    book = session.query(Book).filter_by(id=id).one()
    return jsonify(book=book.serialize)
@app.route('/cataloghome/JSON')
def categoriesJSON():
    categories = session.query(BookCategory).all()
    return jsonify(categories=[i.serialize for i in categories])


# Showing all Book Categories
@app.route('/')
@app.route('/cataloghome/')
def showcatalog():
    categories=session.query(BookCategory).all()
    return render_template('home.html',categories=categories)


@app.route('/cataloghome/<int:bookcategory_id>/')
@app.route('/cataloghome/<int:bookcategory_id>/book')
def cataloghome(bookcategory_id):
    bookcategory = session.query(BookCategory).filter_by(id=bookcategory_id).one()
    items = session.query(Book).filter_by(bookcategory_id=bookcategory.id).all()
    return render_template('catalog.html', bookcategory=bookcategory, items=items)

# Creating a new book in a category
@app.route('/cataloghome/<int:bookcategory_id>/newbook', methods=['GET', 'POST'])
def newBook(bookcategory_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newEntry = Book(name=request.form['name'], 
                   author=request.form['author'],description=request.formd
                        ['description'], reviews=request.form['reviews'],
                        bookcategory_id=bookcategory_id,
                        user_id=login_session['user_id'])
        session.add(newEntry)
        session.commit()
        flash('New Book %s Successfully created' % newEntry.name)
        return redirect(url_for('cataloghome', bookcategory_id=bookcategory_id))
    else:
        return render_template('newbook.html', bookcategory_id=bookcategory_id)

# Editing a book in a category
@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/editbook', methods=['GET', 'POST'])
def editBook(bookcategory_id, id):
    if 'username' not in login_session:
        return redirect('/login')
    editedBook = session.query(Book).filter_by(id=id).one()
    if editedBook.user_id != login_session['user_id']:
        flash('You cannot edit "%s". Please create your own book' %editedBook.name)
        return redirect(url_for('showcatalog')) 
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['reviews']:
            editedBook.reviews = request.form['reviews']
        session.add(editedBook)
        session.commit()
        flash("the book is edited successfully!")
        return redirect(url_for('cataloghome', bookcategory_id=bookcategory_id))
    else:
        return render_template('editbook.html', bookcategory_id=bookcategory_id, id=id, item=editedBook)

# Deleting a book in a category
@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/deletebook', methods=['GET', 'POST'])
def deleteBook(bookcategory_id, id):
    if 'username' not in login_session:
        return redirect('/login')
    booktoDelete = session.query(Book).filter_by(id=id).one()
    if booktoDelete.user_id != login_session['user_id']:
         flash('You cannot delete "%s". Please create your own book' %booktoDelete.name)
         return redirect(url_for('showcatalog')) 
    if request.method == 'POST':
        session.delete(booktoDelete)
        session.commit()
        flash("Book successfully deleted")
        return redirect(url_for('cataloghome', bookcategory_id=bookcategory_id))
    else:
        return render_template('deletebook.html', item=booktoDelete)


if __name__ == '__main__':
    app.secret_key = 'top_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)