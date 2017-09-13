from os import environ

from flask import Flask
import mongoengine

from .resources import articles


mongoengine.connect('default', host=environ['MONGO_URI'])

api = Flask(__name__)
api.register_blueprint(articles.endpoints)