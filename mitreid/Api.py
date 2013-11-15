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

__author__ = 'Tomas Neme'
__maintainer__ = 'Tomas Neme'
__email__ = 'lacrymology@gmail.com'

from mitreid.Client import client_factory
from mitreid.Token import token_factory


class Api(object):
    """
    Main interface class. Use like:

    .. code-block:: python

       >>> from mitreid.Api import Api
       >>> api = Api(token, 'oidc.example.com')
       >>> api.Client.clients_list()
       [[Client: id client-id client-name], [Client: ....]...]
       >>> client = api.Client.get("id")
       >>> client.scope.append('foo')
       >>> client.save()
       >>> token = api.Token.create("client-id")

    """
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
        :param accessToken: an accessToken string that identifies the requesting
            user

        :param oidcHost: the domain (+ optionally base path) of your OIDC server.
            If your API lives in example.com/foo/idoic, set this to
            ``'example.com/foo'``

        """
        self.oidcHost = oidcHost
        self.root = 'https://{}'.format(self.oidcHost)
        self.Token = token_factory(self)
        self.token = self.Token(accessToken=accessToken)
        self.Client = client_factory(self)

    def defaultGrantedScopes(self):
        """
        Returns the list of scopes to be granted to newly created tokens
        and clients default

        """
        return self.defaultScopes

    def defaultGrantedPersonas(self):
        """
        Returns the list of personas to be granted to newly created tokens by
        default

        """
        return self.defaultPersonas
