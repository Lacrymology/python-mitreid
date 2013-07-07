# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Token
   :platform: Unix
   :synopsis: Token class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
import json
from mitreid.base import BaseApi


def token_factory(api):
    class Token(BaseApi):
        """
        OAuth Token class.

        Call Token.create(clientId) to create a Token on behalf of a client.
        Call token.revoke() (or delete()) to revoke this token
        To get a Token's details, you need to do:
            token = Token(accessToken=<access token>)
            token.load_details() (or .read())
        """
        _DEFAULTS = {
            "clientId": "",
            "grantedScopes": api.defaultGrantedScopes(),
            "grantedPersonas": api.defaultGrantedPersonas(),
            "accessToken": "",
            "accessTokenExpiresAt": None
        }

        _API_ROOT = '/idoic/tokenapi'

        _ENDPOINTS = {
            'create': ('post', ''),
            'read': ('get', ''),
            'delete': ('delete', ''),
        }

        def __init__(self, *args, **kwargs):
            return super(Token, self).__init__(api, *args, **kwargs)

        @classmethod
        def create(cls, clientId, grantedScopes=None, grantedPersonas=None):
            """
            Create a new Token on behalf of client `clientId`

            If called with None (default), grantedScopes and grantedPersonas
            will be set to the defaults defined by the Api instance. If you want
            to grant no scopes or personas, pass empty lists instead
            """
            if grantedScopes is None:
                grantedScopes = api.defaultGrantedScopes()
            if grantedPersonas is None:
                grantedPersonas = api.defaultGrantedPersonas()

            # make sure we don't have an id
            method, endpoint = cls._get_endpoint('create')
            res = method(endpoint, data={ 'clientId': clientId,
                                          'grantedPersonas': grantedPersonas,
                                          'grantedScopes': grantedScopes })
            if not res.ok:
                res.raise_for_error()
            attrs = json.loads(res.content)

            # create with server response
            return cls(attrs)

        def read(self):
            """
            Loads self with info from the server. Only the clientToken property
            needs to be filled in. Everything else will be overriden with the
            data from the server
            """
            method, endpoint = self._get_endpoint('read')
            res = method(endpoint)
            if not res.ok:
                res.raise_for_error()
            attrs = json.loads(res.content)

            self._fromdict(attrs)

        def load_details(self):
            return self.read()

        def delete(self):
            """
            Revokes this Token
            """
            method, endpoint = self._get_endpoint('delete')
            res = method(endpoint, data=self._todict(['clientId',
                                                      'clientToken']))
            if not res.ok:
                res.raise_for_error()

            # remove this instance's id
            self.id = None

        def revoke(self):
            return self.delete()
