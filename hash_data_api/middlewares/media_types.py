import logging
import falcon
import ujson
import json

class JSONLD(object):

  def process_request(self, req, resp):
    if req.client_accepts_json:

      if req.method in ('PATCH', 'POST', 'PUT'):
        if 'application/json' not in req.content_type:
          raise falcon.HTTPUnsupportedMediaType(
            'This API only supports requests encoded as JSON.',
            href='http://docs.examples.com/api/json')

      # req.stream corresponds to the WSGI wsgi.input environ variable,
      # and allows you to read bytes from the request body.
      #
      # See also: PEP 3333
      if req.content_length in (None, 0):
        # Nothing to do
        return

      body = req.stream.read()
      if not body:
        raise falcon.HTTPBadRequest('Empty request body',
                                    'A valid JSON document is required.')

      try:
        req.context['doc'] = ujson.loads(body.decode('utf-8'))
      except (ValueError, UnicodeDecodeError):
        raise falcon.HTTPError(falcon.HTTP_753,
                               'Malformed JSON',
                               'Could not decode the request body. The '
                               'JSON was incorrect or not encoded as '
                               'UTF-8.')

  def process_response(self, req, resp, resource):
    if 'data' not in req.context:
      return
    
    resp.body = ujson.dumps({'data': req.context['data']}, ensure_ascii=False)

  @staticmethod
  def error_serializer(req, resp, exception):
    # if req.client_accepts_json:
    logging.exception('message')
    resp.content_type = 'application/json'
    resp.body = ujson.dumps({
        'error': exception.to_dict(),
      }, ensure_ascii=False)