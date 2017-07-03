from time import time
from hashlib import md5
# TODO use pylibmc
import memcache
from pprint import pprint

class CacheMiddleware(object):

  def __init__(self, system_name, connection_info=None):
    self.cache = memcache.Client(['127.0.0.1:11211'], debug=0)

  def _generateHash(self, data):
    h = md5()
    h.update(str(data).encode('utf-8'))
    return h.hexdigest()

  def get(self, id):
    return self.cache.get(id)

  def set(self, id, obj):
    return self.cache.set(id, obj)

  def delete(self, id):
    return self.cache.delete(id)

  def incr(self, id):
    return self.cache.incr(id)

  def decr(self, id):
    return self.cache.decr(id)
  
  def process_request(self, req, resp):
    pass

  def process_response(self, req, resp, resource):
    resp.cache_control = ['max-age=6000']
    resp.etag = self._generateHash(time())
