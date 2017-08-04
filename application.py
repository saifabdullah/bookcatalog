from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_database_setup import Base,  BookCategory, Book

app = Flask(__name__)

engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	
	items = session.query(Book).all()
	
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

if __name__ ==  '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=5000)
