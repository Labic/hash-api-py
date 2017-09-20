# -*- coding: utf-8 -*-
import mongoengine as mongo
from mongoengine.queryset.visitor import Q
import marshmallow as marshal
import msgpack

class AudioSchema(marshal.Schema):
  url = marshal.fields.Url()
  # dateCreated = marshal.fields.DateTime('iso8601')


class AuthorSchema(marshal.Schema):
  # type = marshal.fields.String()
  name = marshal.fields.String()


class Article(mongo.Document):
  articleBody   = mongo.fields.StringField()
  audio         = mongo.fields.DictField(default=None)
  author        = mongo.fields.ListField(mongo.fields.DictField(), 
                                         default=None)
  dateCreated   = mongo.fields.DateTimeField()
  dateModified  = mongo.fields.DateTimeField()
  datePublished = mongo.fields.DateTimeField()
  description   = mongo.fields.StringField()
  image         = mongo.fields.ListField(mongo.fields.StringField(), 
                                         default=None)
  keywords      = mongo.fields.ListField(mongo.fields.StringField(),
                                         default=None)
  headline      = mongo.fields.StringField(db_field='name')
  url           = mongo.fields.URLField()
  metadata      = mongo.fields.DictField(db_field='meta', default=None)

  meta = {
    'collection': 'Article',
    'strict': False,
  }

  @mongo.queryset_manager
  def objects(doc_cls, queryset):
    return queryset.filter(Q(metadata__removed=False) 
                           | Q(metadata__removed__exists=False))\
                   .order_by('-dateCreated', 'datePublished', 'headline')
                   

  class Schema(marshal.Schema):
    id            = marshal.fields.String()
    articleBody   = marshal.fields.String()
    audio         = marshal.fields.Nested(AudioSchema, missing=None)
    author        = marshal.fields.Nested(AuthorSchema, many=True, missing=None)
    dateCreated   = marshal.fields.DateTime()
    dateModified  = marshal.fields.DateTime()
    datePublished = marshal.fields.DateTime()
    description   = marshal.fields.String()
    headline      = marshal.fields.String()
    image         = marshal.fields.List(marshal.fields.String)
    keywords      = marshal.fields.List(marshal.fields.String)
    url           = marshal.fields.Url()
    meta          = marshal.fields.Dict(load_from='metadata')
    
    class Meta:
      strict = True
      ordered = True
      dateformat = 'iso8601'
