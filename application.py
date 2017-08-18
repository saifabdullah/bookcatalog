from flask import Flask, render_template, request, redirect, url_for
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



@app.route('/cataloghome/<int:bookcategory_id>/new',methods=['GET', 'POST'])
def newBook(bookcategory_id):
	if request.method == 'POST':
		newEntry = Book(name=request.form['name'],author=request.form['author'],
		description=request.form['author'],reviews=request.form['reviews'],
		bookcategory_id=bookcategory_id)
		session.add(newEntry)
		session.commit()
		return redirect(url_for('cataloghome',bookcategory_id=bookcategory_id))
	else:
		return render_template('newbook.html',bookcategory_id=bookcategory_id)  

@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/editbook')

def editBook(bookcategory_id, id):
    return "page to edit a book."


@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/deletebook')

def deleteBook(bookcategory_id, id):
    return "page to delete a book."

if __name__ ==  '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)






