from flask import Flask, render_template, request, redirect, url_for, jsonify , flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_database_setup import Base,  BookCategory, Book
 
engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
 # New imports for creating anti-forgery state token
from flask import  session as login_session
import random, string

app = Flask(__name__)

# Making an API endpoint for books from one category
@app.route('/cataloghome/<int:bookcategory_id>/books/JSON/')
def catalogJSON(bookcategory_id):
	bookcategory = session.query(BookCategory).filter_by(id=
		bookcategory_id).one()
	items = session.query(Book).filter_by(bookcategory_id=bookcategory_id).all()
	return jsonify(Books=[i.serialize for i in items])

# Making an API endpoint for a certain book in a category
@app.route('/cataloghome/<int:bookcategory_id>/books/<int:id>/JSON/')
def bookJSON(bookcategory_id,id):
	book = session.query(Book).filter_by(id=id).one()
	
	return jsonify(book=book.serialize)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	return "The session state is %s" % login_session['state']

 
def cataloghome(bookcategory_id):
 	
  	bookcategory = session.query(BookCategory).filter_by(id=bookcategory_id).one()
  	items = session.query(Book).filter_by(bookcategory_id=bookcategory.id)
  	return render_template('catalog.html', bookcategory=bookcategory,items=items)



@app.route('/cataloghome/<int:bookcategory_id>/newbook',methods=['GET', 'POST'])
def newBook(bookcategory_id):
	if request.method == 'POST':
		newEntry = Book(name=request.form['name'],author=request.form['author'],
		description=request.form['description'],reviews=request.form['reviews'],
		bookcategory_id=bookcategory_id)
		session.add(newEntry)
		session.commit()
		flash('New Book %s Successfully created' % newEntry.name)
		return redirect(url_for('cataloghome',bookcategory_id=bookcategory_id))
	else:
		return render_template('newbook.html',bookcategory_id=bookcategory_id)  

@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/editbook',methods=['GET','POST'])

def editBook(bookcategory_id, id):
    editedBook = session.query(Book).filter_by(id=id).one()
    if request.method == 'POST':
    	if request.form ['name']:
    		editedBook.name  = request.form['name']
    	if request.form ['author']:
    		editedBook.author = request.form['author']
    	if request.form['description']:
    		editedBook.description = request.form['description']
    	if request.form['reviews']:
    		editedBook.reviews = request.form['reviews']
    	session.add(editedBook)
    	session.commit()
    	flash("the book is edited successfully!")
        return redirect(url_for('cataloghome',bookcategory_id=bookcategory_id))

    else:
        return render_template('editbook.html',bookcategory_id=bookcategory_id,id=id,item=editedBook)


@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/deletebook',methods=['GET', 'POST'])

def deleteBook(bookcategory_id, id):
	booktoDelete = session.query(Book).filter_by(id=id).one()
	if request.method == 'POST':
		session.delete(booktoDelete)
		session.commit()
		flash("Book successfully deleted")
		return redirect(url_for('cataloghome',bookcategory_id=bookcategory_id))
	else :
		return render_template('deletebook.html',item=booktoDelete)





if __name__ ==  '__main__':
	app.secret_key = 'top_secret_key'
	app.debug = True
	app.run(host='0.0.0.0',port=5000)



