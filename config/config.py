#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   30 Aug 2021
#

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os

app_name = 'SecureNotes'

# Flask related config

app = Flask(app_name)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

app.config['SECRET_KEY'] = 's3_b4nd_$_1'

app.logger.debug('Flask application root path: %s' % app.root_path)
app.logger.debug('Flask application static folder: %s' % app.static_folder)
app.logger.debug('Flask application template folder: %s' % os.path.join(app.root_path, app.template_folder))

# sqlalchemy related config

engine = create_engine('sqlite:///db/secure_notes.db')

Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
