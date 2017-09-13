import mongoengine

from ..server import api


@api.errorhandler(mongoengine.errors.ValidationError)
def handle_bad_request(e):
  return { 'code': 402, 'message': 'bad request' }

@api.errorhandler(mongoengine.errors.LookUpError)
def field_bad_request(e):
  return { 'code': 402, 'message': 'bad request' }

@api.errorhandler(Exception)
def generic_exception_handler(e):
  return { 'code': 500, 'message': 'Sorry! Some bad happen!' }