#!/usr/bin/python
#activate_this = '/var/www/catalog/venv/bin/activate_this.py'
#execfile(activate_this)
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/catalog/')

from catalog import app as application
application.secret_key = 'top_secret_key'
