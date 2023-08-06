__author__ = 'Loris Mularoni'


# Import modules
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# Create the application
app = Flask(__name__)
# db = SQLAlchemy(app)


import regulome_app.webapp.views
