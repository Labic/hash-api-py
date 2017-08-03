import logging; logger = logging.getLogger(__name__)
import falcon

class Articles(object):

  name='Article'

  def __init__(self, datasource):
    self.datasource = datasource

  def on_get(self, req, resp):
    try:
      filters = []; append2filters = filters.append
      
      dateCreated   = req.get_param_as_time_interval('filters[dateCreated]')
      datePublished = req.get_param_as_time_interval('filters[datePublished]')
      keywords      = req.get_param_as_list('filters[keywords]') or ()
      fields        = req.get_param_as_list('fields') or ()
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
        # distinct_on = ['url'],
        order=['-dateCreated'])

      req.context['data'] = [ {
          'id': x.get('_id'),
          'headline': x.get('name'),
          'url': x.get('url'),
          'datePublished': x['datePublished'].isoformat() if 'datePublished' in x else None,
          'dateCreated': x['dateCreated'].isoformat() if 'dateCreated' in x else None,
          'image': x.get('image')[0],
          'articleBody': x.get('articleBody'),
          'description': x.get('description'),
          'keywords': x.get('keywords'),
        } for x in query]
        # TODO: implement fetch im mongo dat source
        # } for x in query.fetch(limit=100)]
    except Exception as e:
      logger.error(e)
      # TODO Add a better descriptions of the error
      raise falcon.HTTPInternalServerError()
