from os import environ

from flask import Flask
import mongoengine as mongo

from .http import Response
from .resource import error
from .resource.article import ArticleResource


mongo.connect('default', host=environ['MONGO_URI'])

api = Flask(__name__)
api.config["APPLICATION_ROOT"] = ''
api.response_class = Response
api.register_blueprint(ArticleResource.blueprint_v1)
api.register_blueprint(error.blueprint)