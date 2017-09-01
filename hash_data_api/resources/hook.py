# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

__all__ = ['HookEvernote']


class HookEvernote(object):

  def on_get(self, req, resp):
    print(req)
