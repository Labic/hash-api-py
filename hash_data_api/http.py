# -*- coding: utf-8 -*-
import flask
import marshmallow

class Response(flask.Response):
  
  default_status = 200
  default_mimetype = 'application/json'

  @classmethod
  def force_type(cls, rv, environ=None):
    if isinstance(rv, Exception):
      rv = flask.jsonify(rv)
    else:
      rv = flask.jsonify(rv)
    return super(Response, cls).force_type(rv, environ)
