# -*- coding: utf-8 -*-

# Copyright (C) 2013 the Institute for Institutional Innovation by Data
# Driven Design Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE MASSACHUSETTS INSTITUTE OF
# TECHNOLOGY AND THE INSTITUTE FOR INSTITUTIONAL INNOVATION BY DATA
# DRIVEN DESIGN INC. BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.
# #
# Except as contained in this notice, the names of the Institute for
# Institutional Innovation by Data Driven Design Inc. shall not be used in
# advertising or otherwise to promote the sale, use or other dealings
# in this Software without prior written authorization from the
# Institute for Institutional Innovation by Data Driven Design Inc.

"""
.. module::
   :platform: Unix
   :synopsis: Default base class for API classes

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>
"""

__author__ = 'Tomas Neme'
__maintainer__ = 'Tomas Neme'
__email__ = 'lacrymology@gmail.com'

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

    def __init__(self, attrs=None, **kwargs):
        """
        attrs can be a dictionary of values to override the defaults, or
        the fields can be passed as keyword arguments.

        Keyword arguments take precedence before the attrs dictionary
        """
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
        return f, "{}{}{}".format(cls._api.root, # https://example.com
                                  cls._API_ROOT, # /path/to/(clients|tokenapi)
                                  endpoint       # /{id}
                                  ).format(**fmt)

    @classmethod
    def _get_headers(cls, extra=None):
        if extra is None:
            extra = {}
        headers = {'Authorization': 'Bearer ' + cls._api.token.accessToken}
        headers.update(extra)
        return headers
