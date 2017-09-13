# -*- coding: utf-8 -*-
from functools import wraps
import datetime as dt
import json
import logging; logger = logging.getLogger(__name__)

import marshmallow
from marshmallow import fields
from mongoengine import Document, errors
from mongoengine.fields import *
from mongoengine.queryset import queryset_manager, DoesNotExist

from flask import Blueprint, request, jsonify, after_this_request

endpoints = Blueprint('articles', __name__, url_prefix='/articles')

# TODO: Move to extension!
from iso8601utils import parsers

class ArticleModel(Document):
  # __slots__ = ('id', 'articleBody', 'author', 'dateCreated', 
  #              'dateModified', 'datePublished', 'description', 
  #              'description', 'image', 'keywords', 'name', 'url', 'meta',)
  
  articleBody   = StringField()
  audio         = DictField(default=None)
  author        = ListField(DictField(), default=None)
  dateCreated   = DateTimeField()
  dateModified  = DateTimeField()
  datePublished = DateTimeField()
  description   = StringField()
  image         = ListField(StringField())
  keywords      = ListField(StringField())
  headline      = StringField(db_field='name')
  url           = URLField()

  meta = {
    'collection': 'Article',
    'strict': False,
  }

  @queryset_manager
  def objects(doc_cls, queryset):
    return queryset.order_by('-dateCreated')


class AudioSchema(marshmallow.Schema):
  url = marshmallow.fields.Url()
  # dateCreated = marshmallow.fields.DateTime('iso8601')


class AuthorSchema(marshmallow.Schema):
  # type = marshmallow.fields.String()
  name = marshmallow.fields.String()

class ArticleResource(object):
  
  class SchemaJSON(marshmallow.Schema):
    id            = fields.String()
    articleBody   = fields.String()
    audio         = fields.Nested(AudioSchema, missing=None)
    author        = fields.Nested(AuthorSchema, many=True, missing=None)
    dateCreated   = fields.DateTime()
    dateModified  = fields.DateTime()
    datePublished = fields.DateTime()
    description   = fields.String()
    headline      = fields.String()
    image         = fields.List(fields.String)
    keywords      = fields.List(fields.String)
    url           = fields.Url()
    
    class Meta:
      ordered = True
      dateformat = 'iso8601'

  # TODO: make generict and move to extension!, can
  def browse_query_string(f):
      @wraps(f)
      def map_query_string(*args, **kwargs):
        filter = {}
        fields = {}
        page = {}
        sort = []
        
        if u'filter[dateCreated]' in request.full_path:
          interval = parsers.interval(request.args.get('filter[dateCreated]', 'P1W'))
          filter['dateCreated__gte'] = interval.start
          filter['dateCreated__lte'] = interval.end
        if u'filter[dateModified]' in request.full_path:
          interval = parsers.interval(request.args.get('filter[dateModified]', 'P1W'))
          filter['dateModified__gte'] = interval.start
          filter['dateModified__lte'] = interval.end
        if u'filter[datePublished]' in request.full_path:
          interval = parsers.interval(request.args.get('filter[datePublished]', 'P1W'))
          filter['datePublished__gte'] = interval.start
          filter['datePublished__lte'] = interval.end
        if u'filter[keywords]' in request.full_path:
          filter['keywords__in'] = request.args.get('filter[keywords]').split(',')
        
        if u'fields' in request.full_path:
          fields['only'] = request.args.get('fields').split(',')
          fields['exclude']: ['articleBody']
        
        if u'page' in request.full_path:
          page['skip'] = int(request.args.get('page[skip]', 0))
          page['limit'] = int(request.args.get('page[limit]', 10))
        
        if u'sort' in request.full_path:
          sort += request.args.get('sort').split(',')
        return f(filter=filter ,fields=fields, page=page, sort=sort, *args, **kwargs)

      return map_query_string

  # READ: https://gist.github.com/knzm/fa35b391af94d5eb701d
  # https://flask-restless.readthedocs.io/en/stable/index.html  
  # https://www.programcreek.com/python/example/67050/flask.request.path
  # Extend flask.Route?
  @endpoints.route('', methods=['GET'])
  @browse_query_string
  def browse(filter: dict = {}, 
             fields: dict = {}, 
             page: dict = {},
             sort: list = (),
             **kwargs):
    result = ArticleModel.objects(**filter)\
                         .order_by(*sort)\
                         .only(*fields.get('only', []))\
                         .exclude(*fields.get('exclude', ['articleBody']))\
                         .skip(page.get('skip', 0))\
                         .limit(page.get('limit', 10))

    # data, errors = ArticleResource.schemas['many'].dump(result, update_fields=False,)
    # data, errors = ArticleResource.OwnSchema(many=True, only=fields, exclude=['articleBody'])\
    data, errors = ArticleResource.SchemaJSON(many=True, 
                                              only=fields.get('only'),
                                              exclude=fields.get('exlude', ['articleBody']),)\
                                  .dump(result)
    return jsonify({'data': data})

  @endpoints.route('/<id>', methods=['GET'])
  def read(id: str):
    try:
      result = ArticleModel.objects.get(id=id)
      data, errors = ArticleResource.SchemaJSON()\
                                    .dump(result)
      return jsonify(data)
    except ValidationError as e:
      return jsonify({
        'code': 400,
        'message': ('ID parameter is not a valid on path, it must be a 12-byte'
                   'input or a 24-character hex string')
      })

  @endpoints.route('/<id>', methods=['DELETE'])
  def delete(id: str):
    result = ArticleModel.objects.get(id=id)
    data, errors = ArticleResource.SchemaJSON()\
                                  .dump(result)
    return jsonify(data)


from werkzeug.exceptions import BadRequest

@endpoints.errorhandler(errors.ValidationError)
def handle_bad_request(e):
  return BadRequest()

@endpoints.errorhandler(errors.LookUpError)
def field_bad_request(e):
  return BadRequest()

@endpoints.errorhandler(Exception)
def generic_exception_handler(e):
  return jsonify({ 'code': 500, 'message': 'Sorry! Some bad happen!' })