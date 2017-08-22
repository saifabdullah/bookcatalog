from flask import Flask, render_template, request, redirect, url_for, jsonify , flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_database_setup import Base,  BookCategory, Book
 
app = Flask(__name__)
 
engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
@app.route('/cataloghome/')
@app.route('/')

def home():
	categories =session.query(BookCategory).all()
	items = session.query(Book).all()
	return render_template('home.html',categories=categories,items=items)


     
@app.route('/cataloghome/<int:bookcategory_id>/')
 
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
		flash("new book created!")
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
		return render_template('deleteconfirmation.html',item=booktoDelete)
	else :
		return render_template('deletebook.html',item=booktoDelete)



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

if __name__ ==  '__main__':
	app.secret_key = 'top_secret_key'
	app.debug = True
	app.run(host='0.0.0.0',port=5000)



