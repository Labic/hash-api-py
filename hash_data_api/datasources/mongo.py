from os import environ
import signal
from datetime import datetime

from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

class MongoDatasource(object):

  def __init__(self):
    self.client = MongoClient(environ['MONGO_URI'])
    self.db = self.client.get_default_database()
    signal.signal(signal.SIGTERM, self._signal_term_handler)

  def _signal_term_handler(self, signal, frame):
    self.client.close()

  def query(self, **kargs):
    collection = self.db[kargs['kind']]

    filter = {}
    for f in kargs.get('filters', ()):
      property, operator, value = f
      
      # TODO: find a better way to discover tha is array
      if operator == '=' and not '[]' in property:
        filter[property] = value

      if operator == '=' and '[]' in property:
        property = property.replace('[]', '')
        if not filter.get(property):
          filter[property] = {'$all': []}
        # TODO: find a better way to deal with arrays
        filter[property]['$all'].append(value)
      
      if operator == '>' and isinstance(value, datetime):
        filter[property] = {
          '$gte': value,
        }
      
      if operator == '<' and isinstance(value, datetime):
        if '$gte' in filter[property]:
          filter[property] = {**filter[property], **{'$lte': value}}
        else:
          filter[property] = {'$lte': value}

    sort = []; append2sort = sort.append
    for o in kargs.get('order', ()):
      direction = DESCENDING if o[:1] == '-' else ASCENDING
      property  = o.replace('-', '')
      append2sort((property, direction))

    if !kargs.get('fields'):
      kargs['fields'] = None 
    
    return collection.find(
      filter=filter, 
      projection=kargs['fields'],
      skip=kargs['skip'],
      limit=kargs['limit'],
      sort=sort,)

  def fetch(self, id):
    pass
