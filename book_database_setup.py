#importing default os, sys and specific packages of sqlalchemy module to build the database 

import os 
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class BookCategory(Base):

	#creating Bookcategory class and table in the database.

	__tablename__ = 'bookcategory'

	id = Column(Integer,primary_key=True)
	name =  Column(String(250),nullable=False)

	

class Book(Base):

	""" creating Book class and table in the database. """

	__tablename__ = 'book'

	name = Column(String(300),nullable = False)
	id = Column(Integer,primary_key = True)
	author = Column(String(400),nullable = False)
	# ratings =  Column(float, nullable = False) cannot make the float datatype declaration in sqlalchemy
	description = Column(String(500),nullable = False)
	reviews = Column(String(500))
	bookcategory_id = Column(Integer,ForeignKey('bookcategory.id'))
	bookcategory = relationship(BookCategory)

	@property
	def serialize(self):
		# Returns object data in easily serializeable format
		return {
			'name'	: self.name,
			'id' : self.id,
			'author' : self.author,
			'description' : self.description,
			'reviews' : self.reviews,
		}

engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.create_all(engine)