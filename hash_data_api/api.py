from os import environ

import falcon
from falcon_cors import CORS

from middlewares.http import Request
from middlewares.media_types import JSONLD
from middlewares.cache import CacheMiddleware
from datasources import DatasourceEngine
from resources import article, hook, oauth

cors = CORS(
  allow_all_origins=True,
  allow_all_methods=True,
)

server = falcon.API(
  request_type=Request,
  middleware=[
    # CacheMiddleware('memcached'),
    cors.middleware,
    JSONLD(),
  ])
server.set_error_serializer(JSONLD.error_serializer)

# db = DatasourceEngine('GCP_DATASTORE')
datasource = DatasourceEngine('MONGO')
# files = StorageEngine('google-cloud-storage', credentias='AWS_S3_CREDENTIALS')

oAuthEvernote = oauth.OAuthEvernote()
server.add_route('/articles', article.Collection(datasource=datasource))
server.add_route('/articles/{id}', article.Item(datasource=datasource))
server.add_route('/hooks/evernote', hook.HookEvernote())
# server.add_route('/oauths/evernote', oauth.Evernote)
# server.add_route('/oauths/evernote/callback', oAuthEvernote)

if __name__ == '__main__':
  """
  This is used when running locally. Gunicorn is used to run the
  application on Cloud.
  """
  from wsgiref import simple_server

  httpd = simple_server.make_server('127.0.0.1', 5000, server)
  httpd.serve_forever()