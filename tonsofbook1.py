from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_database_setup import Book, Base, BookCategory, User

engine = create_engine('postgresql+psycopg2://catalog:1234@localhost/bookcatalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(name="Essentialist_Saif", email="saifab@gmail.com",
             picture=' https://lh6.googleusercontent.com/-xUvnyEVUegE/AAAAAAAAAAI/AAAAAAAAAnk/jLSvRK-3K8I/photo.jpg')
session.add(User1)
session.commit()
# Books for History  & Autobiography category

category1= BookCategory(user_id=1,name="History & autobiograpy")

session.add(category1)
session.commit()




book2  = Book(user_id=1,name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book2)
session.commit()

book3  = Book(user_id=1,name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book3)
session.commit()


book4  = Book(user_id=1,name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book4)
session.commit()


book5  = Book(user_id=1,name="A Long Walk to Freedom", author="x", description= "y",   reviews= "z", bookcategory= category1 ) 

session.add(book5)
session.commit()


category2= BookCategory(user_id=1,name="Technology")

session.add(category2)
session.commit()


book1 = Book(user_id=1,name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book1)
session.commit()


book2 = Book(user_id=1,name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book2)
session.commit()

book3 = Book(user_id=1,name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book3)
session.commit()

book4 = Book(user_id=1,name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book4)
session.commit()

book5 = Book(user_id=1,name="Learn Python the hard way",author="x",description="y",reviews="z", bookcategory=category2)
session.add(book5)
session.commit()


category3= BookCategory(user_id=1,name="Language & Culture")

session.add(category3)
session.commit()

book1= Book(user_id=1,name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book1)
session.commit()

book2= Book(user_id=1,name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book2)
session.commit()

book3= Book(user_id=1,name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book3)
session.commit()

book4= Book(user_id=1,name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book4)
session.commit()

book5= Book(user_id=1,name="Letters to My daughter",author="x", description="y", reviews="z",bookcategory=category3)

session.add(book5)
session.commit()


print "added books!"
