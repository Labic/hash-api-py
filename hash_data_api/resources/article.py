# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

import falcon

__all__ = ['Article', 'Item']


class Collection(object):

  name = 'Article'

  def __init__(self, datasource):
    self.datasource = datasource

  def on_get(self, req, resp):
    try:
      filters = [('meta.deleted', '', {'$in': [None, False]})]
      append2filters = filters.append
      
      dateCreated   = req.get_param_as_time_interval('filters[dateCreated]')
      datePublished = req.get_param_as_time_interval('filters[datePublished]')
      keywords      = req.get_param_as_list('filters[keywords]') or ()
      fields        = req.get_param_as_list('fields') or []
      page          = req.get_param_as_int('page') or 1
      per_page      = req.get_param_as_int('per_page') or 10

      if dateCreated is not None:
        append2filters(('dateCreated', '>', dateCreated.start))
        append2filters(('dateCreated', '<', dateCreated.end))
      if datePublished is not None:
        append2filters(('datePublished', '>', datePublished.start))
        append2filters(('datePublished', '<', datePublished.end))
      if keywords:
        # FIXME use map or list compresion
        # [append2filters(('keywords', '=', k)) for k in keywords]
        # TODO: implement a better way to find that is an array in query
        [append2filters(('keywords[]', '=', k)) for k in keywords]
      
      query = self.datasource.query(
        kind=self.name, 
        filters=filters, 
        fields=fields, 
        skip=0 if page == 1 else page * per_page, 
        limit=per_page, 
        order=['-dateCreated'])

      if not fields:
        req.context['data'] = [{
            'id': str(x.get('_id')),
            'headline': x.get('name', None),
            'url': x.get('url', None),
            'datePublished': x['datePublished'].isoformat() if 'datePublished' in x else None,
            'dateCreated': x['dateCreated'].isoformat() if 'dateCreated' in x else None,
            'dateModified': x['dateModified'].isoformat() if 'dateModified' in x else None,
            'image': x.get('image', [None])[0],
            'articleBody': x.get('articleBody', None),
            'audio': x.get('audio', None),
            'description': x.get('description', None),
            'keywords': x.get('keywords', None),
          } for x in query]
      else:
        data = []; append2data = data.append
        for x in query:
          o = {'id': str(x['_id'])}
          
          for f in fields:
            if f == 'datePublished' and 'datePublished' in x:
              o[f] = x[f].isoformat()
            elif f == 'dateCreated' and 'dateCreated' in x:
              o[f] = x[f].isoformat()
            elif f == 'dateModified' and 'dateModified' in x:
              o[f] = x[f].isoformat()
            else:
              if f in x:
                o[f] = x[f]

          append2data(o)

        req.context['data'] = data
    
    except Exception as e:
      logger.error(e)
      # TODO Add a better descriptions of the error
      raise falcon.HTTPInternalServerError()


class Item:

  name = 'Article'

  def __init__(self, datasource):
    self.datasource = datasource

  def on_get(self, req, resp, id):
    fields = req.get_param_as_list('fields') or ()
    
    item = self.datasource.lookup(kind=self.name, 
                                  id=id,
                                  fields=fields,)

    item['id'] = str(item.get('_id'))[0],
    del item['_id']
    if 'dateCreated' in item:
      item['dateCreated'] = item['dateCreated'].isoformat()
    if 'datePublished' in item:
      item['datePublished'] = item['datePublished'].isoformat()
    if 'dateModified' in item:
      item['dateModified'] = item['dateModified'].isoformat()
    if 'image' in item:
      item['image'] = item['image'][0]
    if 'name' in item:
      item['headline'] = item['name']
      del item['headline']

    req.context['data'] = item
  
  def on_delete(self, req, resp, id):
    result = self.datasource.patch(kind=self.name, 
                                   id=id,
                                   properties={
                                      '$set': {'meta.deleted': True}
                                   })
    resp.status = '204 No Content'