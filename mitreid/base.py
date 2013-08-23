# -*- coding: utf-8 -*-

"""
.. module:: mitreid.base
   :platform: Unix
   :synopsis: Default base class for API classes

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
import copy
import requests

class BaseApiObject(object):
    """
    * _DEFAULTS is a dictionary are the default values for the subclass. It's
      keys list is used to build the dictionary to be passed as data to the
      requests
    * _API_ROOT is the root path the endpoints are based of.
    * _ENDPOINTS is the list of endpoints in this form: {
            action: (http method, /endpoint/path),
            }. /endpoint/path is based on _API_ROOT.
      For example, with API_ROOT=/api/clients, { 'update': ('put', '/{id}')} will
      make a PUT request to /api/clients/{id}
    """
    _DEFAULTS = {}
    _API_ROOT = ''
    _ENDPOINTS = {}

    def __init__(self, api, attrs=None, **kwargs):
        """
        attrs can be a dictionary of values to override the defaults, or
        the fields can be passed as keyword arguments.

        Keyword arguments take precedence before the attrs dictionary
        """
        self._api = api
        d = copy.deepcopy(self._DEFAULTS)
        if attrs:
            d.update(attrs)
        d.update(kwargs)

        self._fromdict(d)

    def _todict(self, attributes_list=None):
        if attributes_list is None:
            attributes_list = self._DEFAULTS.keys()
        ret = {}
        for k in attributes_list:
            try:
                ret[k] = getattr(self, k)
            except AttributeError:
                pass
        return ret

    def _fromdict(self, attrs):
        for k, v in attrs.items():
            setattr(self, k, v)

    @classmethod
    def _get_endpoint(cls, endpoint, fmt=None):
        if fmt is None:
            fmt = {}
        method, endpoint = cls._ENDPOINTS[endpoint]
        f = getattr(requests, method.lower())
        return f, (cls._API_ROOT + endpoint).format(**fmt)

    def _auth(self):
        return self._api.token
