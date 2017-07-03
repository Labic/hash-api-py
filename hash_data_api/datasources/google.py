from google.cloud import datastore

class GCPDatastoreDatasource(object):

  def __init__(self):
    return datastore.Client()