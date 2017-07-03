import falcon

class CommonFilters(object):
  
  def process_request(self, req, resp):
    req.get_param

  def process_response(self, req, resp, resource):
    if 'data' not in req.context:
      return
    
    resp.body = ujson.dumps({ 'data': req.context['data'] }, 
                            double_precision=4, ensure_ascii=False)
