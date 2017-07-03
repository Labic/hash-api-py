import falcon
from iso8601utils import parsers

class Request(falcon.Request):

  def get_param_as_time_interval(self, name, required=False, store=None):
    params = self._params
    
    if name in params:
      interval = parsers.interval(params[name])
      
      return interval

    if not required:
      return None

    raise errors.HTTPMissingParam(name)
