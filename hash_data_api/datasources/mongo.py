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
    for f in kargs['filters']:
      property = f[0]
      operator = f[1]
      value    = f[2]
      
      # TODO: find a better way to discover tha is array
      if operator == '=' and not '[]' in property:
        filter[property] = value

      if operator == '=' and '[]' in property:
        property = property.replace('[]', '')
        if not filter.get(property):
          filter[property] = {'$in': []}
        # TODO: find a better way to deal with arrays
        filter[property]['$in'].append(value)
      
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
    for o in kargs['order']:
      direction = DESCENDING if o[:1] == '-' else ASCENDING
      property  = o.replace('-', '')
      
      append2sort((property, direction))

    print(filter)
    return collection.find(filter=filter, sort=sort)

  def fetch(self, **kargs):
    pass
