# -*- coding: utf-8 -*-

"""
.. module:: mitreid.Client
   :platform: Unix
   :synopsis: Client class

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""

import copy
import requests

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

