# -*- coding: utf-8 -*-
from flask import Blueprint

from ..model import Article
from .base import query_string


class ArticleResource(object):

  blueprint_v1 = Blueprint('article', __name__, url_prefix='/v1/articles')

  # @credentials('articles.browse.*')
  @blueprint_v1.route('', methods=['GET'])
  @query_string
  def browse(filters={}, fields=[], sort=['-dateCreated'], page={}):
    """
    TODO: resolve this
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
    """
    result = Article.objects(**filters)\
                    .only(*fields)\
                    .exclude(*['articleBody'])\
                    .order_by(*sort)\
                    .skip(page.get('skip', 0))\
                    .limit(page.get('limit', 10))

    data, errors = Article.Schema(many=True, 
                                  only=fields,
                                  exclude=['articleBody'])\
                          .dump(result)
    return { 'data': data } 

  @blueprint_v1.route('/<id>', methods=['GET'])
  @query_string
  def read(id: str, fields=[]):
    instance = Article.objects.only(*fields)\
                              .get(id=id)
    
    data = Article.Schema(only=fields).dump(instance)
    return data

  @blueprint_v1.route('/<id>', methods=['PATCH'])
  def edit(id: str, instance: Article=None):
    instance = Article.objects.get(id=id)
    data = Article.Schema().dump(instance)
    # instance.update()
    return data

  @blueprint_v1.route('', methods=['POST'])
  def add(instance: Article=None):
    instance.save()
    data = Article.Schema().dump(instance)
    return data, 201

  @blueprint_v1.route('/<id>', methods=['DELETE'])
  def delete(id: str):
    instance = Article.objects.get(id=id)
    instance.update(metadata__removed=True)
    return True, 204