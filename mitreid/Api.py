# -*- coding: utf-8 -*-

"""
.. module:: 
   :platform: Unix
   :synopsis: TODO

.. moduleauthor:: Tomas Neme <lacrymology@gmail.com>

"""
from mitreid.Client import client_factory
from mitreid.Token import token_factory


class Api(object):
    defaultScopes = [
        'openid',
        'profile',
        'email',
        'address',
        'phone',
        # 'offline_access',
    ]
    defaultPersonas = ['Home', 'Work', 'Mobile']
    def __init__(self, accessToken, oidcHost):
        """
        `accessToken` is an accessToken string that identifies the requesting
        user
        """
        self.oidcHost = oidcHost
        self.root = 'https://{}'.format(self.oidcHost)
        self.Token = token_factory(self)
        self.token = self.Token(accessToken=accessToken)
        self.Client = client_factory(self)

    def defaultGrantedScopes(self):
        return self.defaultScopes

    def defaultGrantedPersonas(self):
        return self.defaultPersonas
