from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_database_setup import Book, Base, BookCategory

engine = create_engine('sqlite:///bookcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Books for History  & Autobiography category

category1= BookCategory(name="History & autobiograpy")

session.add(category1)
session.commit()

book1  = Book(name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book1)
session.commit()

print "added books!"