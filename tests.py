import unittest

from mitreid.Api import Api
from mitreid.exceptions import MitreIdException

TOKEN = """eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjEzNzg0NzQyMzQsImF1ZCI6WyJpZDMtb2ljLWRlbW8tY2xpZW50Il0sImlzcyI6Imh0dHBzOlwvXC9sb2dydXMuaWRoeXBlcmN1YmVkLm9yZ1wvaWRvaWNcLyIsImp0aSI6IjY5OTcwODRhLTExMTMtNDRiMi05MDhmLTUwOWRmZTUwZGIyMSIsImlhdCI6MTM3NDg3NDIzNH0.B01BHN82r34_WFSiLkzFH5pOs-brXJT5_lkwnGXfQqepVO1jgX0W3dJgsr8fqC5cWWISxbV6Mx76udnWYiRVDWUEdUL2KgMltZIXqgy5ru8TmL9USw0hXFarAmcANyOM8cyF2lvT2qCUeW_Dda7X3g8nhV_U4ceFrtF6jJK3WLc"""
SCOPES_FOR_TOKEN = ['address', 'email', 'openid', 'phone', 'profile',
                    'superclient']
PERSONAS_FOR_TOKEN = []
CLIENT_ID_FOR_TOKEN = 'id3-oic-demo-client'
USER_FOR_TOKEN = 'admin'

class ClientCreationDeletionTestCase(unittest.TestCase):

    def test_create_and_delete(self):
        '''
        Test the creation and deletion of a client
        '''
        api = Api(TOKEN)
        client = api.Client(clientId='test_client', clientSecret='password')
        client.save()

        # created
        self.assertIsNotNone(client.id)

        client.delete()

        # deleted
        self.assertRaises(MitreIdException, api.Client.read, client.id)

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        '''
        Create a per-test client
        '''
        self.api = Api(TOKEN)
        self.client = self.api.Client(clientId='test_client',
                                      clientSecret='password',
                                      scope=['foo', 'bar'])
        self.client.save()

    def tearDown(self):
        '''
        Delete the per-test client
        '''
        self.client.delete()

    def test_clients_list(self):
        '''
        Test fetching of the list of clients
        '''
        clients = self.api.Client.clients_list()
        self.assertGreaterEqual(len(clients), 1)
        for c in clients:
            self.assertIsInstance(c, self.api.Client)
            self.assertIsNotNone(c.id)

    def test_read(self):
        '''
        Test reading of a client
        '''
        client1 = self.api.Client.clients_list()[-1]
        client2 = self.api.Client.read(client1.id)
        c1 = client1._todict()
        c2 = client2._todict()
        self.assertDictEqual(c1, c2)

    def test_update(self):
        '''
        Test updating of a client attribute
        '''
        new_id = 'test_client_renamed'
        self.client.clientId = new_id
        self.client.save()

        client2 = self.api.Client.read(self.client.id)
        self.assertEqual(client2.clientId, new_id)

    def test_add_scope(self):
        '''
        Test addition of one scope
        '''
        self.client.add_scopes('baz')
        self.client.save()
        client2 = self.api.Client.read(self.client.id)
        scopes = client2.scope[:]
        scopes.sort()
        self.assertEqual(scopes, ['bar', 'baz', 'foo'])

    def test_add_scopes(self):
        '''
        Test addition of more than one scope
        '''
        self.client.add_scopes(['baz', 'bleh'])
        self.client.save()
        client2 = self.api.Client.read(self.client.id)
        scopes = client2.scope[:]
        scopes.sort()
        self.assertEqual(scopes, ['bar', 'baz', 'bleh', 'foo'])

    def test_remove_scope(self):
        '''
        Test removal of one scope
        '''
        self.client.remove_scopes('bar')
        self.client.save()
        client2 = self.api.Client.read(self.client.id)
        self.assertEqual(client2.scope, ['foo'])

    def test_remove_scopes(self):
        '''
        Test removal of more than one scope
        '''
        self.client.remove_scopes(['foo', 'bar'])
        self.client.save()
        client2 = self.api.Client.read(self.client.id)
        self.assertEqual(client2.scope, [])

class TokenTestCase(unittest.TestCase):

    def setUp(self):
        '''
        Create a per-test API object
        '''
        self.api = Api(TOKEN)

    def test_create_and_delete(self):
        '''
        Test the creation a deletion of a token
        '''
        client_id = 'test_client'
        personas = ['Mobile']
        scopes = ['phone']
        client = self.api.Client(clientId=client_id,
                                 clientSecret='password',
                                 scope=scopes)
        client.save()
        t = self.api.Token.create(client_id,
                                  grantedScopes=scopes,
                                  grantedPersonas=personas)

        self.assertEqual(t.clientId, client_id)
        for scope in scopes:
            self.assertIn(scope, t.authorizedScopesSet)
        self.assertEqual(t.authorizedPersonaSet, personas)

        t.delete()
        client.delete()

    def test_read(self):
        '''
        Test reading a token
        '''
        client_id = 'test_client'
        personas = ['Mobile']
        scopes = ['phone']
        client = self.api.Client(clientId=client_id,
                                 clientSecret='password',
                                 scope=scopes)
        client.save()
        t = self.api.Token.create(client_id,
                                  grantedScopes=scopes,
                                  grantedPersonas=personas)

        token = self.api.Token.read(t.accessToken)
        for scope in scopes:
            self.assertIn(scope, token.authorizedScopesSet)
        self.assertEqual(token.authorizedPersonaSet, personas)
        self.assertGreater(len(token.accessToken), 0)
        self.assertIsNotNone(token.accessTokenExpiresAt)
        self.assertEqual(token.clientId, client_id)
        self.assertGreater(len(token.authorizingUser), 0)

        t.delete()
        client.delete()

    def test_read_default(self):
        '''
        Test reading the default token
        '''
        token = self.api.Token.read()
        self.assertEqual(token.authorizedScopesSet, SCOPES_FOR_TOKEN)
        self.assertEqual(token.authorizedPersonaSet, PERSONAS_FOR_TOKEN)
        self.assertEqual(token.accessToken, TOKEN)
        self.assertIsNotNone(token.accessTokenExpiresAt)
        self.assertEqual(token.clientId, CLIENT_ID_FOR_TOKEN)
        self.assertEqual(token.authorizingUser, USER_FOR_TOKEN)

if __name__ == '__main__':
    unittest.main()
