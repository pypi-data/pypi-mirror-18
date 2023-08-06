# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import unittest

import mock
from requests.exceptions import RequestException

from dlogr.clients import DlogrClient
from dlogr.exceptions import DlogrAPIError


@mock.patch('dlogr.clients.requests')
class DlogrModelMixinTestCase(unittest.TestCase):
    def test_resource_list_events(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.list()

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params={'limit': 30, 'offset': 0},
            verify=mock.ANY,
        )

    def test_resource_list_customers(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Customer.list()

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/customers',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params={'limit': 30, 'offset': 0},
            verify=mock.ANY,
        )

    def test_resource_list_auth_token(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_token='weirdhashhere')
        client.Event.list()

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY, 'Authorization': 'Token weirdhashhere'},
            data=None,
            params={'limit': 30, 'offset': 0},
            verify=mock.ANY,
        )

    def test_resource_list_auth_credentials(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_credentials=('my@email.com', 'sikret'))
        client.Event.list()

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=('my@email.com', 'sikret'),
            headers={'user-agent': mock.ANY},
            data=None,
            params={'limit': 30, 'offset': 0},
            verify=mock.ANY,
        )

    def test_resource_list_request_error(self, requests_patched):
        requests_patched.get.side_effect = RequestException('API is acting up!')
        client = DlogrClient('http://api.dlogr.com')

        with self.assertRaises(DlogrAPIError) as context:
            client.Event.list()
        self.assertEquals('{}'.format(context.exception), 'API is acting up!')

    def test_resource_list_additional_parameters(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.list(fields='unicorn', answer=42)

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params={'limit': 30, 'offset': 0, 'fields': 'unicorn', 'answer': 42},
            verify=mock.ANY,
        )

    def test_resource_list_limit_offset(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.list(limit=100, offset=50)

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params={'limit': 100, 'offset': 50},
            verify=mock.ANY,
        )


@mock.patch('dlogr.clients.requests')
class DlogrClientCreateTestCase(unittest.TestCase):
    def test_resource_create_events(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.create(email='super@email.com', password='sikret', name='Hamster')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'super@email.com', 'password': 'sikret', 'name': 'Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_create_customers(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Customer.create(email='super@email.com', password='sikret', name='Hamster')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/customers',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'super@email.com', 'password': 'sikret', 'name': 'Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_create_auth_token(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_token='weirdhashhere')
        client.Event.create(email='super@email.com', password='sikret', name='Hamster')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={'user-agent': mock.ANY, 'Authorization': 'Token weirdhashhere'},
            data={'email': 'super@email.com', 'password': 'sikret', 'name': 'Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_create_auth_credentials(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_credentials=('my@email.com', 'sikret'))
        client.Event.create(email='super@email.com', password='sikret', name='Hamster')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=('my@email.com', 'sikret'),
            headers={'user-agent': mock.ANY},
            data={'email': 'super@email.com', 'password': 'sikret', 'name': 'Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_create_request_error(self, requests_patched):
        requests_patched.post.side_effect = RequestException('API is acting up!')
        client = DlogrClient('http://api.dlogr.com')

        with self.assertRaises(DlogrAPIError) as context:
            client.Event.create(email='super@email.com', password='sikret', name='Hamster')
        self.assertEquals('{}'.format(context.exception), 'API is acting up!')


@mock.patch('dlogr.clients.requests')
class DlogrClientRetrieveTestCase(unittest.TestCase):
    def test_resource_retrieve_events(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.retrieve('object_id')

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_retrieve_customers(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Customer.retrieve('object_id')

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/customers/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_retrieve_auth_token(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_token='weirdhashhere')
        client.Event.retrieve('object_id')

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY, 'Authorization': 'Token weirdhashhere'},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_retrieve_auth_credentials(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_credentials=('my@email.com', 'sikret'))
        client.Event.retrieve('object_id')

        requests_patched.get.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=('my@email.com', 'sikret'),
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_retrieve_request_error(self, requests_patched):
        requests_patched.get.side_effect = RequestException('API is acting up!')
        client = DlogrClient('http://api.dlogr.com')

        with self.assertRaises(DlogrAPIError) as context:
            client.Event.retrieve('object_id')
        self.assertEquals('{}'.format(context.exception), 'API is acting up!')


@mock.patch('dlogr.clients.requests')
class DlogrClientUpdateTestCase(unittest.TestCase):
    def test_resource_update_events(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.update('object_id', email='new@email.com', name='New Hamster')

        requests_patched.patch.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'new@email.com', 'name': 'New Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_update_customers(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Customer.update('object_id', email='new@email.com', name='New Hamster')

        requests_patched.patch.assert_called_once_with(
            'http://api.dlogr.com/api/customers/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'new@email.com', 'name': 'New Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_update_auth_token(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_token='weirdhashhere')
        client.Event.update('object_id', email='new@email.com', name='New Hamster')

        requests_patched.patch.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY, 'Authorization': 'Token weirdhashhere'},
            data={'email': 'new@email.com', 'name': 'New Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_update_auth_credentials(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_credentials=('my@email.com', 'sikret'))
        client.Event.update('object_id', email='new@email.com', name='New Hamster')

        requests_patched.patch.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=('my@email.com', 'sikret'),
            headers={'user-agent': mock.ANY},
            data={'email': 'new@email.com', 'name': 'New Hamster'},
            params=None,
            verify=mock.ANY,
        )

    def test_resource_update_request_error(self, requests_patched):
        requests_patched.patch.side_effect = RequestException('API is acting up!')
        client = DlogrClient('http://api.dlogr.com')

        with self.assertRaises(DlogrAPIError) as context:
            client.Event.update('object_id', email='new@email.com', name='New Hamster')
        self.assertEquals('{}'.format(context.exception), 'API is acting up!')


@mock.patch('dlogr.clients.requests')
class DlogrClientDeleteTestCase(unittest.TestCase):
    def test_resource_delete_events(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Event.delete('object_id')

        requests_patched.delete.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_delete_customers(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')
        client.Customer.delete('object_id')

        requests_patched.delete.assert_called_once_with(
            'http://api.dlogr.com/api/customers/object_id',
            auth=None,
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_delete_auth_token(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_token='weirdhashhere')
        client.Event.delete('object_id')

        requests_patched.delete.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=None,
            headers={'user-agent': mock.ANY, 'Authorization': 'Token weirdhashhere'},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_delete_auth_credentials(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com', auth_credentials=('my@email.com', 'sikret'))
        client.Event.delete('object_id')

        requests_patched.delete.assert_called_once_with(
            'http://api.dlogr.com/api/events/object_id',
            auth=('my@email.com', 'sikret'),
            headers={'user-agent': mock.ANY},
            data=None,
            params=None,
            verify=mock.ANY,
        )

    def test_resource_delete_request_error(self, requests_patched):
        requests_patched.delete.side_effect = RequestException('API is acting up!')
        client = DlogrClient('http://api.dlogr.com')

        with self.assertRaises(DlogrAPIError) as context:
            client.Event.delete('object_id')
        self.assertEquals('{}'.format(context.exception), 'API is acting up!')


@mock.patch('dlogr.clients.requests')
class DlogClientAuthTestCase(unittest.TestCase):
    def test_login(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')

        client.Auth.login(email='my@email.com', password='password')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/auth/login',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'my@email.com', 'password': 'password'},
            params=None,
            verify=mock.ANY,
        )

    def test_verify_account(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')

        client.Auth.verify_account(token='wildhash')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/auth/verify-account',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'token': 'wildhash'},
            params=None,
            verify=mock.ANY,
        )

    def test_reset_password(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')

        client.Auth.reset_password(email='my@email.com')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/auth/reset-password',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'my@email.com'},
            params=None,
            verify=mock.ANY,
        )

    def test_change_password(self, requests_patched):
        client = DlogrClient('http://api.dlogr.com')

        client.Auth.change_password(email='my@email.com', password='pwd', new_password='better', reset_token='hashhh')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/auth/change-password',
            auth=None,
            headers={'user-agent': mock.ANY},
            data={'email': 'my@email.com', 'password': 'pwd', 'new_password': 'better', 'reset_token': 'hashhh'},
            params=None,
            verify=mock.ANY,
        )
