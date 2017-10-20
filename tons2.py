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

engine = create_engine('postgresql://catalog:saif@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

print "added!"from flask import Flask, render_template, request, redirect, url_for, \
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

engine = create_engine('postgresql://catalog:saif@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

print "added!"
