from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, flash
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
    open('/var/www/bcl2/client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Book Catalog Application"

engine = create_engine('postgresql://catalog:1234@localhost/bookcatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.rollback()
