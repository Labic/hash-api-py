# -*- coding: utf-8 -*-
import abc
import logging; logger = logging.getLogger(__name__)
import datetime as dt
import typing

import marshmallow
from mongoengine import *
from mongoengine.queryset import queryset_manager, DoesNotExist
from apistar import http, Route, typesystem

__all__ = ['ArticleResource']

class ArticleModel(Document):
  # __slots__ = ('id', 'articleBody', 'author', 'dateCreated', 
  #              'dateModified', 'datePublished', 'description', 
  #              'description', 'image', 'keywords', 'name', 'url', 'meta',)
  
  articleBody   = StringField()
  author        = ListField(DictField())
  audio         = DictField()
  dateCreated   = DateTimeField(default=dt.datetime.utcnow)
  dateModified  = DateTimeField()
  datePublished = DateTimeField()
  description   = StringField()
  image         = ListField(StringField())
  images_to_download_urls = ListField(StringField())
  keywords      = ListField(StringField())
  name          = StringField()
  url           = URLField()

  meta = {
    'collection': 'Article',
  }

  @queryset_manager
  def objects(doc_cls, queryset):
      # This may actually also be done by defining a default ordering for
      # the document, but this illustrates the use of manager methods
      return queryset.order_by('-dateCreated')

class AudioSchema(marshmallow.Schema):
  url = marshmallow.fields.Url()
  dateCreated = marshmallow.fields.DateTime('iso8601')

class ArticleSchema(marshmallow.Schema):
  id            = marshmallow.fields.String()
  articleBody   = marshmallow.fields.String()
  author        = marshmallow.fields.List(marshmallow.fields.Dict)
  audio         = AudioSchema()
  dateCreated   = marshmallow.fields.DateTime('iso8601')
  dateModified  = marshmallow.fields.DateTime('iso8601')
  datePublished = marshmallow.fields.DateTime('iso8601')
  description   = marshmallow.fields.String()
  name          = marshmallow.fields.String(dump_to='headline')
  image         = marshmallow.fields.List(marshmallow.fields.String)
  images_to_download_urls = marshmallow.fields.List(marshmallow.fields.String)
  keywords      = marshmallow.fields.List(marshmallow.fields.String)
  url           = marshmallow.fields.Url()
  
  # @marshmallow.post_load
  # def create(self, data):
  #   return ArticleModel(**data)

# class AuthorSchema(typesystem.Object):
#   properties={
#     'type': typesystem.string(default=None),
#     'name': typesystem.string(default=None),
#   }

# class ArticleSchema(typesystem.Object):
#     properties = {
#         # 'id': typesystem.Object(),
#         # 'articleBody': typesystem.string(default=None),
#         'author': typesystem.array(items=AuthorSchema),
#         'dateCreated': typesystem.string(format='datetime', default=None),
#         'dateModified': typesystem.string(format='datetime', default=None),
#         'datePublished': typesystem.string(format='datetime', default=None),
#         'description': typesystem.string(default=None),
#         'name': typesystem.string(default=None),
#         # 'headline': typesystem.string(),
#         'image': typesystem.array(items=typesystem.string(), default=None),
#         'keywords': typesystem.array(items=typesystem.string(), default=None),
#         'url': typesystem.string(),
#     }


class ArticleResource(object):

  # async def browse(fields: str, page: int = 1, per_page: int = 25,):
  def browse(fields: str, page: int = 1, per_page: int = 25,):
    page = page or 1
    per_page = per_page or 25
    skip = 0 if page == 1 else page * per_page
    if fields:
      result = ArticleModel.objects()\
                           .only(fields)\
                           .skip(skip)\
                           .limit(per_page)
    else:
      result = ArticleModel.objects()\
                           .exclude(('articleBody'))\
                           .skip(skip)\
                           .limit(per_page)

    data, errors = ArticleSchema(many=True).dump(result)
    return data
    # return [ArticleSchema(record.to_mongo().to_dict()) for record in result]

  # async def read(id: str):
  def read(id: str):
    result = ArticleModel.objects.get(id=id)
    data, errors = ArticleSchema().dump(result)
    return data

  # async def add(article: ArticleSchema):
  #   ArticleSchema.save()
  #   return ArticleSchema().dump(article)

  # async def edit(id: str, article: http.RequestData):
  def edit(id: str, article: http.RequestData):
    try:
      ArticleModel.objects.get(id=id)\
                          .update(**article)
    except DoesNotExist:
      return http.Response(status=404, headers={'Content-Type': 'application/json'})
    
    return http.Response(status=204, headers={u'Content-Type': 'application/json'})

  # async def delete(id: str) -> dict:
  def delete(id: str) -> dict:
    try:
      result = ArticleModel.objects.get(id=id)
      result.delete()
    except DoesNotExist:
      return http.Response(status=404)
    
    return http.Response(None, status=204)

  routes = [
    Route('articles', 'GET', browse),
    Route('articles/{id}', 'GET', read),
    # Route('articles', 'POST', add),
    Route('articles/{id}', 'PATCH', edit),
    Route('articles/{id}', 'DELETE', delete),
  ]