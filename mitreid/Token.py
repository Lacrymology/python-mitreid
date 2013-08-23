# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Token
   :platform: Unix
   :synopsis: Token class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
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
        _DEFAULTS = {
            "authorizedScopesSet": api.defaultGrantedScopes(),
            "authorizedPersonaSet": api.defaultGrantedPersonas(),
            "accessToken": "",
            "accessTokenExpiresAt": None,
            "clientId": "",
            "authorizingUser": ""
        }

        _API_ROOT = 'https://{host}/idoic/tokenapi'

        _ENDPOINTS = {
            'create': ('POST',   ''),
            'read':   ('GET',    ''),
            'delete': ('DELETE', ''),
        }

        def __init__(self, *args, **kwargs):
            super(Token, self).__init__(api, *args, **kwargs)

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
            data = json.dumps({'clientId': clientId,
                               'grantedPersonas': grantedPersonas,
                               'grantedScopes': grantedScopes})
            headers = {'Authorization': 'Bearer ' + api.token.accessToken,
                       'Content-Type': JSON_MEDIA_TYPE}
            method, endpoint = cls._get_endpoint('create',
                                                 {'host': api.oidcHost})
            res = method(endpoint, data=data, headers=headers, verify=False)
            if res.status_code != 200:
                raise MitreIdException
            attrs = json.loads(res.content)

            # create with server response
            return cls(attrs)

        @classmethod
        def read(cls, token=None):
            """
            Loads self with info from the server. Only the clientToken property
            needs to be filled in. Everything else will be overriden with the
            data from the server
            """
            if token is None:
                token = api.token.accessToken
            headers = {'Authorization': 'Bearer ' + token}
            method, endpoint = cls._get_endpoint('read',
                                                 {'host': api.oidcHost})
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
            headers = {'Authorization': 'Bearer ' + api.token.accessToken,
                       'Content-Type': JSON_MEDIA_TYPE}
            method, endpoint = self._get_endpoint('delete',
                                                  {'host': api.oidcHost})
            res = method(endpoint, data=data, headers=headers, verify=False)
            if res.status_code != 200:
                raise MitreIdException
        revoke = delete

        def __repr__(self):
            return '[Token: %s...%s %s]' % (self.accessToken[:10],
                                            self.accessToken[-10:],
                                            self.clientId)

    return Token
