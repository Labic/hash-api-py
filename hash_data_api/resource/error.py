# -*- coding: utf-8 -*-
import flask
import mongoengine as mongo

__all__ = ['blueprint', 'BaseError', 'BadRequest', 'NotFound'
           'InternalServerError']

blueprint = flask.Blueprint('error_handlers', __name__)


class BaseError(Exception):
  
  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.payload = payload
    self.message = message
    if status_code is not None:
      self.status_code = status_code

  def to_dict(self):
    rv = dict(self.payload or ())
    rv['code'] = self.status_code
    rv['message'] = self.message
    return rv, self.status_code


class BadRequest(BaseError):
  status_code = 400


class NotFound(BaseError):
  status_code = 404


class InternalServerError(BaseError):
  status_code = 500


@blueprint.app_errorhandler(mongo.errors.DoesNotExist)
def _not_found(e):
  message = 'ID not found, maybe it was already deleted'
  return NotFound(message).to_dict()

@blueprint.app_errorhandler(500)
def _internal_server_error(e):
  message = ('Something wrong has happened to us, '
             'do not worry, it\'s not your fault.')
  return InternalServerError(message).to_dict()
