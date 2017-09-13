import json
import unittest

from hash_data_api import server

class ArticlesRestfullCase(unittest.TestCase):

  def setUp(self):
    server.api.testing = True
    self.api = server.api.test_client()
    # with flaskr.app.app_context():
    #   flaskr.init_db()

  def assert_status_code_and_content_type(self, 
                                          resp,
                                          status_code, 
                                          content_type):
    self.assertEqual(resp.status_code, status_code)
    self.assertEqual(resp.headers['Content-Type'], content_type)

  def test_get_without_parameters(self):
    resp = self.api.get('/articles')
    data = json.loads(resp.data)

    self.assert_status_code_and_content_type(resp, 200, 'application/json')
    self.assertEqual(len(data['data']), 10)
    for article in data['data']:
      self.assertIn('id', article)
      self.assertNotIn('articleBody', article)
      self.assertIn('audio', article)
      self.assertIn('author', article)
      self.assertIn('dateCreated', article)
      self.assertIn('dateModified', article)
      self.assertIn('datePublished', article)
      self.assertIn('description', article)
      self.assertIn('headline', article)
      self.assertIn('image', article)
      self.assertIn('keywords', article)
      self.assertIn('url', article)

  def test_get_with_parameter_page_limit(self):
    def assert_fields(data):
      for article in data['data']:
        self.assertIn('id', article)
        self.assertNotIn('articleBody', article)
        self.assertIn('audio', article)
        self.assertIn('author', article)
        self.assertIn('dateCreated', article)
        self.assertIn('dateModified', article)
        self.assertIn('datePublished', article)
        self.assertIn('description', article)
        self.assertIn('headline', article)
        self.assertIn('image', article)
        self.assertIn('keywords', article)
        self.assertIn('url', article)
    
    resp1 = self.api.get('/articles?page[limit]=1')
    resp2 = self.api.get('/articles?page[limit]=8')
    data1 = json.loads(resp1.data)
    data2 = json.loads(resp2.data)

    self.assert_status_code_and_content_type(resp1, 200, 'application/json')
    self.assert_status_code_and_content_type(resp2, 200, 'application/json')
    self.assertEqual(len(data1['data']), 1)
    self.assertEqual(len(data2['data']), 8)
    assert_fields(data1)
    assert_fields(data2)

  def test_get_with_parameter_fields(self):
    resp1 = self.api.get('/articles?fields=url')
    resp2 = self.api.get('/articles?fields=headline,dateCreated')
    resp3 = self.api.get('/articles?fields=id,author')
    data1 = json.loads(resp1.data)
    data2 = json.loads(resp2.data)
    data3 = json.loads(resp3.data)

    self.assert_status_code_and_content_type(resp1, 200, 'application/json')
    self.assert_status_code_and_content_type(resp2, 200, 'application/json')
    self.assert_status_code_and_content_type(resp3, 200, 'application/json')

    self.assertEqual(len(data1['data']), 10)
    self.assertEqual(len(data2['data']), 10)
    self.assertEqual(len(data3['data']), 10)
    for article in data1['data']:
      self.assertNotIn('id', article)
      self.assertNotIn('articleBody', article)
      self.assertNotIn('audio', article)
      self.assertNotIn('author', article)
      self.assertNotIn('dateCreated', article)
      self.assertNotIn('dateModified', article)
      self.assertNotIn('datePublished', article)
      self.assertNotIn('description', article)
      self.assertNotIn('headline', article)
      self.assertNotIn('image', article)
      self.assertNotIn('keywords', article)
      self.assertIn('url', article)
    for article in data2['data']:
      self.assertNotIn('id', article)
      self.assertNotIn('articleBody', article)
      self.assertNotIn('audio', article)
      self.assertNotIn('author', article)
      self.assertIn('dateCreated', article)
      self.assertNotIn('dateModified', article)
      self.assertNotIn('datePublished', article)
      self.assertNotIn('description', article)
      self.assertIn('headline', article)
      self.assertNotIn('image', article)
      self.assertNotIn('keywords', article)
      self.assertNotIn('url', article)
    for article in data3['data']:
      self.assertIn('id', article)
      self.assertNotIn('articleBody', article)
      self.assertNotIn('audio', article)
      self.assertIn('author', article)
      self.assertNotIn('dateCreated', article)
      self.assertNotIn('dateModified', article)
      self.assertNotIn('datePublished', article)
      self.assertNotIn('description', article)
      self.assertNotIn('headline', article)
      self.assertNotIn('image', article)
      self.assertNotIn('keywords', article)
      self.assertNotIn('url', article)

if __name__ == '__main__':
  unittest.main()