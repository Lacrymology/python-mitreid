# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Token
   :platform: Unix
   :synopsis: Token class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
from datetime import datetime
import json

from mitreid.base import BaseApiObject
from mitreid.exceptions import MitreIdException

JSON_MEDIA_TYPE = 'application/json'

def token_factory(api):
    class Token(BaseApiObject):
        """
        OAuth Token class.

        Call Token.create(clientId) to create a Token on behalf of a client.
        Call token.revoke() (or delete()) to revoke this token
        To get a Token's details, you need to do:
            token = Token(accessToken=<access token>)
            token.load_details() (or .read())
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
            Create a new Token on behalf of client `clientId`

            If called with None (default), grantedScopes and grantedPersonas
            will be set to the defaults defined by the Api instance. If you want
            to grant no scopes or personas, pass empty lists instead
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
            if res.status_code != 200:
                raise MitreIdException
            attrs = json.loads(res.content)

            # create with server response
            return cls(attrs)

        def save(self):
            """
            If you created a Token by filling in the clientId, grantedScopes and grantedPersonas fields, but
            but leaving the accessToken field empty, this creates a token and fills self in with the data

            if accessToken is present, this is a noop. If anything but clientId is not present, defaults will be used
            """
            if self.accessToken:
                return
            t = self.create(self.clientId, grantedScopes=self.grantedScopes, grantedPersonas=self.grantedPersonas)
            self._fromdict(t._todict())

        @classmethod
        def read(cls, token):
            """
            Returns a Token instance with the data for `token` loaded from the server

            `token` is the accessToken string
            """
            if token is None:
                token = cls._api.token.accessToken
            headers = cls._get_headers({'Authorization': 'Bearer ' + token})
            method, endpoint = cls._get_endpoint('read')

            res = method(endpoint, headers=headers, verify=False)
            if res.status_code != 200:
                raise MitreIdException
            attrs = json.loads(res.content)
            return cls(attrs)
        load_details = read

        def delete(self):
            """
            Revokes this Token
            """
            data = json.dumps({'clientId': self.clientId,
                               'clientToken': self.accessToken})
            headers = self._get_headers(extra={'Content-Type': JSON_MEDIA_TYPE})
            method, endpoint = self._get_endpoint('delete')
            res = method(endpoint, data=data, headers=headers, verify=False)
            if res.status_code != 200:
                raise MitreIdException
        revoke = delete

        def __repr__(self):
            return '[Token: %s...%s %s]' % (self.accessToken[:10],
                                            self.accessToken[-10:],
                                            self.clientId)

    return Token
