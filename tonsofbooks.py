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




book2  = Book(name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book2)
session.commit()

book3  = Book(name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book3)
session.commit()


book4  = Book(name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book4)
session.commit()


book5  = Book(name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book5)
session.commit()


category2= BookCategory(name="Technology")

session.add(category2)
session.commit()


book1 = Book(name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book1)
session.commit()


book2 = Book(name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book2)
session.commit()

book3 = Book(name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book3)
session.commit()

book4 = Book(name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book4)
session.commit()

book5 = Book(name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book5)
session.commit()


category3= BookCategory(name="Language & Culture")

session.add(category3)
session.commit()

book1= Book(name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book1)
session.commit()

book2= Book(name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book2)
session.commit()

book3= Book(name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book3)
session.commit()

book4= Book(name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book4)
session.commit()

book5= Book(name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book5)
session.commit()


print "added books!"