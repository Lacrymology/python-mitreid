# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Client
   :platform: Unix
   :synopsis: Client class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""

import copy
import requests
import json

def client_factory(api):
    class Client(object):
        _DEFAULTS = {
            "id": None,
            "clientId": "",
            "clientSecret": "",
            "generateSecret": True,
            "redirectUris": [],
            "clientName": "",
            "clientUri": None,
            "logoUri": None,
            "contacts": [],
            "tosUri": None,
            "tokenEndpointAuthMethod": None,
            "scope": [
                # "phone",
                # "openid",
                # "offline_access",
                # "address",
                # "email",
                # "profile"
            ],
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
            "allowIntrospection": False,
            "idTokenValiditySeconds": 600,
            "createdAt": None
        }

        _API_ROOT = '/api/clients'

        _ENDPOINTS = {
            'list': ('get', ''),
            'create': ('post', ''),
            'read': ('get', '/{id}'),
            'update': ('put', '/{id}'),
            'delete': ('delete', '/{id}'),
        }

        def __init__(self, attrs=None, **kwargs):
            """
            attrs can be a dictionary of values to override the defaults, or
            the fields can be passed as keyword arguments.

            Keyword arguments take precedence before the attrs dictionary

            If an 'id' attribute is present, the Client is assumed to have a
            server counterpart
            """
            d = copy.deepcopy(self._DEFAULTS)
            if attrs:
                d.update(attrs)
            d.update(kwargs)

            self._fromdict(d)

            # if a clientSecret was provided, we need to override this default
            if self.clientSecret:
                self.generateSecret = False

        def _todict(self):
            ret = {}
            for k in self._DEFAULTS:
                try:
                    ret[k] = getattr(self, k)
                except AttributeError:
                    pass
            return ret

        def _fromdict(self, attrs):
            for k, v in attrs.items():
                setattr(self, k, v)

        @classmethod
        def _get_endpoint(cls, endpoint, fmt):
            method, endpoint = cls._ENDPOINTS[endpoint]
            f = getattr(requests, method)
            return f, endpoint.format(fmt)

        def create(self):
            # make sure we don't have an id
            self.id = None
            method, endpoint = self._get_endpoint('create')
            res = method(endpoint, data=self._todict())
            if not res.ok:
                res.raise_for_error()
            attrs = json.loads(res.content)

            # update with server-created defaults
            self._fromdict(attrs)

        @classmethod
        def read(cls, id):
            """
            Returns a single Client getting it from the server by id
            """
            method, endpoint = cls._get_endpoint('read', {'id': id})
            res = method(endpoint)
            if not res.ok:
                res.raise_for_error()
            attrs = json.loads(res.content)

            return cls(attrs)

        def update(self):
            """
            Updates the server counterpart of this instance with it's current
            attributes
            """
            method, endpoint = self._get_endpoint('update', {'id': self.id})
            res = method(endpoint, data=self._todict())
            if not res.ok:
                res.raise_for_error()

            # update any fields returned from the server
            attrs = json.loads(res.content)
            self._fromdict(attrs)

        def delete(self):
            """
            Deletes the server counterpart of this instance. Does not destroy
            the instance itself, but it removes the id
            """
            method, endpoint = self._get_endpoint('delete', {'id': self.id})
            res = method(endpoint)
            if not res.ok:
                res.raise_for_error()

            # remove this instance's id
            self.id = None

