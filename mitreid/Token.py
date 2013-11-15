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
.. module:: mitreid.Token
   :platform: Unix
   :synopsis: Token class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>
"""

__author__ = 'Tomas Neme'
__maintainer__ = 'Tomas Neme'
__email__ = 'lacrymology@gmail.com'

from datetime import datetime
import json

from mitreid.base import BaseApiObject
from mitreid.exceptions import MitreIdException

JSON_MEDIA_TYPE = 'application/json'

def token_factory(api):
    class Token(BaseApiObject):
        """
        OAuth Token class.

        Call ``Token.create(clientId)`` to create a ``Token`` on behalf of a
        client.
        Call ``token.revoke()`` (or ``delete()``) to revoke this token
        To get a ``Token``'s details, you need to do:
        .. code-block::

            >>> token = Token(accessToken=<access token>)
            >>> token.load_details() # (or .read())

        """
        _api = api
        _DEFAULTS = {
            "authorizedScopesSet": api.defaultGrantedScopes(),
            "authorizedPersonaSet": api.defaultGrantedPersonas(),
            "accessToken": "",
            "accessTokenExpiresAt": None,
            "clientId": "",
            "authorizingUser": ""
        }

        _API_ROOT = '/idoic/tokenapi'

        _ENDPOINTS = {
            'create': ('POST',   ''),
            'read':   ('GET',    ''),
            'delete': ('DELETE', ''),
        }

        def __init__(self, *args, **kwargs):
            super(Token, self).__init__(*args, **kwargs)
            if isinstance(self.accessTokenExpiresAt, basestring):
                # convert this to date
                try:
                    self.accessTokenExpiresAt = datetime.strptime(self.accessTokenExpiresAt, "%Y-%m-%dT%H:%M:%S%z")
                except:
                    ts = self.accessTokenExpiresAt.split('+')[0]
                    self.accessTokenExpiresAt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

        @classmethod
        def create(cls, clientId, grantedScopes=None, grantedPersonas=None):
            """
            Create a new Token on behalf of client ``clientId``

            If called with ``None`` (default), ``grantedScopes`` and
            ``grantedPersonas`` will be set to the defaults defined by the
            ``Api`` instance. If you want to grant no scopes or personas, pass
            empty lists instead

            """
            if grantedScopes is None:
                grantedScopes = cls._api.defaultGrantedScopes()
            if grantedPersonas is None:
                grantedPersonas = cls._api.defaultGrantedPersonas()

            # make sure we don't have an id
            data = json.dumps({'clientId': clientId,
                               'grantedPersonas': grantedPersonas,
                               'grantedScopes': grantedScopes})
            headers = cls._get_headers(extra={'Content-Type': JSON_MEDIA_TYPE})
            method, endpoint = cls._get_endpoint('create')
            res = method(endpoint, data=data, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
            attrs = json.loads(res.content)

            # create with server response
            return cls(attrs)

        def save(self):
            """
            If you created a ``Token`` by filling in the ``clientId``,
            ``grantedScopes`` and ``grantedPersonas`` fields, but leaving the
            ``accessToken`` field empty, this creates a token and fills self in
            with the data

            if ``accessToken`` is present, this is a noop. If anything but
            ``clientId`` is not present, defaults will be used

            """
            if self.accessToken:
                return
            t = self.create(self.clientId, grantedScopes=self.grantedScopes, grantedPersonas=self.grantedPersonas)
            self._fromdict(t._todict())

        @classmethod
        def read(cls, token):
            """
            Returns a ``Token`` instance with the data for ``token`` loaded
            from the server

            :param token: the ``accessToken`` string

            """
            if token is None:
                token = cls._api.token.accessToken
            headers = cls._get_headers({'Authorization': 'Bearer ' + token})
            method, endpoint = cls._get_endpoint('read')

            res = method(endpoint, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
            attrs = json.loads(res.content)
            return cls(attrs)
        load_details = read

        def delete(self):
            """
            Revokes this ``Token``

            """
            data = json.dumps({'clientId': self.clientId,
                               'clientToken': self.accessToken})
            headers = self._get_headers(extra={'Content-Type': JSON_MEDIA_TYPE})
            method, endpoint = self._get_endpoint('delete')
            res = method(endpoint, data=data, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
        revoke = delete

        def __repr__(self):
            return '[Token: %s...%s %s]' % (self.accessToken[:10],
                                            self.accessToken[-10:],
                                            self.clientId)

    return Token
