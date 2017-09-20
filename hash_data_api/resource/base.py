# -*- coding: utf-8 -*-
import re
from functools import wraps

from iso8601utils import parsers
import marshmallow as marshal
from querystring_parser import parser as qs_parser
# from webargs import core
# from webargs.flaskparser import FlaskParser
from flask import request


class CollectionField(marshal.fields.String):
  def _deserialize(self, value, attr, data):
    if value is None:
      return []
    if isinstance(value, list):
      return value
    return value.split(',')


class QueryStringSchema(marshal.Schema):
  
  class PageSchema(marshal.Schema):
    skip = marshal.fields.Integer(missing=0, load_only=True,)
    limit = marshal.fields.Integer(missing=10, load_only=True,)
  
  filters = marshal.fields.Dict()
  fields = CollectionField(format='csv')
  sort = CollectionField(format='csv')
  page = marshal.fields.Nested(PageSchema)

  class Meta:
    strict = True


def query_string(f):
  print(f)
  qs_schema = QueryStringSchema()
  # READ: https://gist.github.com/knzm/fa35b391af94d5eb701d
  # https://flask-restless.readthedocs.io/en/stable/index.html  
  # https://www.programcreek.com/python/example/67050/flask.request.path
  # Extend flask.Route?
  @wraps(f)
  def map_query_string(*args, **kwargs):
    if request.query_string:
      qs = qs_parser.parse(request.query_string)
      qs_serialized = qs_schema.load(qs).data
      return f(*args, **{**kwargs, **qs_serialized})

    return f(*args, **kwargs)

  return map_query_string

# from werkzeug.exceptions import BadRequest

# @blueprint.errorhandler(errors.ValidationError)
# def handle_bad_request(e):
#   return BadRequest()

# @blueprint.errorhandler(errors.LookUpError)
# def field_bad_request(e):
#   return BadRequest()

# @blueprint.errorhandler(Exception)  
# def generic_exception_handler(e):
#   return jsonify({ 'code': 500, 'message': 'Sorry! Some bad happen!' })