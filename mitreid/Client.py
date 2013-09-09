# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Client
   :platform: Unix
   :synopsis: Client class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""

import json

from mitreid.base import BaseApiObject
from mitreid.exceptions import MitreIdException

JSON_MEDIA_TYPE = 'application/json'

def client_factory(api):
    class Client(BaseApiObject):
        _api = api
        _DEFAULTS = {
            "id": None,  # diff
            "clientId": "",  # diff
            "clientSecret": "",  # diff
            "generateSecret": True,  # added
            "redirectUris": [],  # diff
            "clientName": "",  # diff
            "clientUri": None,
            "logoUri": None,
            "contacts": [],
            "tosUri": None,
            "tokenEndpointAuthMethod": None,
            "scope": api.defaultGrantedScopes(),
            "grantTypes": [
                # "implicit",
                # "authorization_code",
                # "urn:ietf:params:oauth:grant_type:redelegate",
                # "refresh_token"
            ],
            "responseTypes": [],
            "policyUri": None,
            "jwksUri": None,
            "applicationType": None,
            "sectorIdentifierUri": None,
            "subjectType": None,
            "requestObjectSigningAlg": None,
            "userInfoSignedResponseAlg": None,
            "userInfoEncryptedResponseAlg": None,
            "userInfoEncryptedResponseEnc": None,
            "idTokenSignedResponseAlg": None,
            "idTokenEncryptedResponseAlg": None,
            "idTokenEncryptedResponseEnc": None,
            "defaultMaxAge": None,
            "requireAuthTime": None,
            "defaultACRvalues": [],
            "initiateLoginUri": None,
            "postLogoutRedirectUri": None,
            "requestUris": [],
            "authorities": [],
            "accessTokenValiditySeconds": 3600,
            "refreshTokenValiditySeconds": None,
            "resourceIds": [],
            "clientDescription": None,
            "reuseRefreshToken": True,
            "dynamicallyRegistered": False,
            "allowIntrospection": True,
            "idTokenValiditySeconds": 600,
            "createdAt": None
        }

        _API_ROOT = '/idoic/api/clients'

        _ENDPOINTS = {
            'list':   ('GET',    ''),
            'create': ('POST',   ''),
            'read':   ('GET',    '/{id}'),
            'update': ('PUT',    '/{id}'),
            'delete': ('DELETE', '/{id}'),
        }

        def __init__(self, attrs=None, **kwargs):
            """
            attrs can be a dictionary of values to override the defaults, or
            the fields can be passed as keyword arguments.

            Keyword arguments take precedence before the attrs dictionary

            If an 'id' attribute is present, the Client is assumed to have a
            server counterpart
            """
            super(Client, self).__init__(attrs=attrs, **kwargs)

            # if a clientSecret was provided, we need to override this default
            if self.clientSecret:
                self.generateSecret = False

        @classmethod
        def clients_list(cls):
            headers = cls._get_headers()
            method, endpoint = cls._get_endpoint('list')
            res = method(endpoint, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
            clients_json = json.loads(res.content)
            return [cls(cj) for cj in clients_json]

        def create(self):
            # make sure we don't have an id
            self.id = None
            data = json.dumps(self._todict())
            headers = self._get_headers(extra={'Content-Type': JSON_MEDIA_TYPE})
            method, endpoint = self._get_endpoint('create')
            res = method(endpoint, data=data, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
            attrs = json.loads(res.content)

            # update with server-created defaults
            self._fromdict(attrs)

        @classmethod
        def read(cls, id):
            """
            Returns a single Client getting it from the server by id
            """
            headers = cls._get_headers()
            method, endpoint = cls._get_endpoint('read', {'id': id})
            res = method(endpoint, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)
            attrs = json.loads(res.content)

            return cls(attrs)
        get = read

        def update(self):
            """
            Updates the server counterpart of this instance with it's current
            attributes
            """
            data = json.dumps(self._todict())
            headers = self._get_headers(extra={'Content-Type': JSON_MEDIA_TYPE})
            method, endpoint = self._get_endpoint('update', {'id': self.id})
            res = method(endpoint, data=data, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)

            # update any fields returned from the server
            attrs = json.loads(res.content)
            self._fromdict(attrs)

        def delete(self):
            """
            Deletes the server counterpart of this instance. Does not destroy
            the instance itself, but it removes the id
            """
            headers = self._get_headers()
            method, endpoint = self._get_endpoint('delete', {'id': self.id})
            res = method(endpoint, headers=headers, verify=False)
            MitreIdException._wrap_requests_response(res)

            # remove this instance's id
            self.id = None

        def save(self):
            """
            Creates or updates in server from self
            """
            if self.id is None:
                return self.create()
            else:
                return self.update()

        def add_scopes(self, scopes):
            """
            Add scopes to Client

            `scopes` can be either a single scope string, or an iterable
            """
            if isinstance(scopes, basestring):
                scopes = [scopes]
            for scope in scopes:
                if scope not in self.scope:
                    self.scope.append(scope)

        def remove_scopes(self, scopes):
            """
            Remove scopes from Client

            `scopes` can be either a single scope string, or an iterable
            """
            if isinstance(scopes, basestring):
                scopes = [scopes]
            for scope in scopes:
                if scope in self.scope:
                    self.scope.remove(scope)

        def __repr__(self):
            return '[Client: %s %s %s]' % (self.id,
                                           self.clientId,
                                           self.clientName)

    return Client
