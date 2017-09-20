# -*- coding: utf-8 -*-
from os import environ
import logging; logger = logging.getLogger(__name__)

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from falcon import HTTPTemporaryRedirect

__all__ = ['OAuthEvernote']


class OAuthEvernote(object):

  def __init__(self, key=None, secret=None, sandbox=True):
    self.key = key if key \
                   else environ.get('EVERNOTE_CONSUMER_KEY', 'gustavorps-7133')
    self.secret = secret if secret \
                         else environ.get('EVERNOTE_CONSUMER_SECRET', 'f94f713717cb45d3')
    self.sandbox = sandbox
    self.client = self.create_client()
    self.callback_path = '/oauths/evernote/callback'
    self.tokens = {}

  def create_client(self, token=None):
    if token:
      return EvernoteClient(token=token, sandbox=self.sandbox)
    else:
      if hasattr(self, 'client'):
        return self.client

      return EvernoteClient(consumer_key=self.key, 
                            consumer_secret=self.secret, 
                            sandbox=self.sandbox)

  def on_get(self, req, resp):
    print()
    if req.path == '/oauths/evernote':
      callback_url = ''.join((req.scheme, '://', req.netloc, self.callback_path))
      self.tokens = self.client.get_request_token(callback_url)
      raise HTTPTemporaryRedirect(self.client.get_authorize_url(self.tokens))
    elif req.path == '/oauths/evernote/callback':
      print(req.context)
      self.client.get_access_token(self.tokens['oauth_token'],
                                   self.tokens['oauth_token_secret'],
                                   req.params.get('oauth_verifier'))
      note_store = self.client.get_note_store()
      note_filter = NoteFilter()
      note_metadata_spec = NotesMetadataResultSpec()
      note_metadata_spec.includeTitle = True
      note_metadata_spec.includeNotebookGuid = True
      note_metadata_spec.includeTagGuids = True
      note_metadata_spec.includeAttributes = True
      note_metadata_spec.includeContentLength = True

      req.context['data'] = {
        'notebooks': note_store.listNotebooks(),
        'notes': note_store.findNotesMetadata(note_filter, 0, 100, note_metadata_spec),
      }