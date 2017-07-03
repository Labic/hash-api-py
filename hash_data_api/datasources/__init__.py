class DatasourceEngine(object):
  
  def __init__(self, dsn, **kargs):
    self._dsn = ''.join(('_DNS_', dsn))
    
    if dsn == 'MONGO':
      from .mongo import MongoDatasource
      self.datasource = MongoDatasource()
    
    if dsn == 'GCP_DATASTORE':
      from .google import GCPDatastoreDatasource
      self.datasource = GCPDatastoreDatasource()

  def query(self, **kargs):
    return self.datasource.query(**kargs)

  def fetch(self, **kargs):
    return self.datasource.fetch(**kargs)