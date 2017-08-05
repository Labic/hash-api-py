from os import environ

import falcon
from falcon_cors import CORS

from middlewares.http import Request
from middlewares.media_types import JSONLD
from middlewares.cache import CacheMiddleware
from datasources import DatasourceEngine
from resources import Article


cors = CORS(
  allow_all_origins=True,
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

server.add_route('/articles', Article(datasource=datasource))

if __name__ == "__main__":
  """
  This is used when running locally. Gunicorn is used to run the
  application on Cloud.
  """
  from wsgiref import simple_server

  httpd = simple_server.make_server('127.0.0.1', 5000, server)
  httpd.serve_forever()