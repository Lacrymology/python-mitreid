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
            'get': ('get', '/{id}'),

        }

        def __init__(self, attrs=None, in_server=False, **kwargs):
            """
            attrs can be a dictionary of values to override the defaults, or
            the fields can be passed as keyword arguments.

            Keyword arguments take precedence before the attrs dictionary

            in_server tells this instance to expect to have a server counterpart
            """
            self.attrs = copy.deepcopy(self._DEFAULTS)
            if attrs:
                self.attrs.update(attrs)
            self.attrs.update(kwargs)
            self._in_server = in_server

        def __getattr__(self, item):
            try:
                return self.attrs[item]
            except KeyError:
                raise (AttributeError,
                       "'{}' object has no attribute '{}'".format(
                           self.__class__, item))
