from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_database_setup import Base,  BookCategory, Book

app = Flask(__name__)

engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

    
@app.route('/cataloghome/<int:bookcategory_id>/')

def cataloghome(bookcategory_id):
	
	bookcategory = session.query(BookCategory).filter_by(id=bookcategory_id).one()
	items = session.query(Book).filter_by(bookcategory_id=bookcategory.id)
	
	output = ''
	for i in items:
		output += i.name 
		output += '</br>'
		output += i.author
		output += '</br>'
		output += i.description
		output += '</br>'
		output += i.reviews
		output += '</br>'
		output += '</br>'
		
	return output

@app.route('/cataloghome/<int:bookcategory_id>/newbook')

def newBook(bookcategory_id):
    return "page to create a new book."


@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/editbook')

def editBook(bookcategory_id, id):
    return "page to edit a book."


@app.route('/cataloghome/<int:bookcategory_id>/<int:id>/deletebook')

def deleteBook(bookcategory_id, id):
    return "page to delete a book."

if __name__ ==  '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)
