from os import environ

from apistar import Include, Route
from apistar.frameworks.asyncio import ASyncIOApp as App
# from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

from mongoengine import connect

from resources import *


connect('document-db', host=environ['MONGO_URI'])

routes = [
  Include('/', ArticleResource.routes),
  Include('/docs', docs_urls),
  Include('/static', static_urls),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
