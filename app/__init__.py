from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
from app import views
