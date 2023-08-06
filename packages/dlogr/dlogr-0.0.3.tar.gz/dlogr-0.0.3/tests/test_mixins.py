# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import os
import unittest

from freezegun import freeze_time
import mock

from dlogr.mixins import DlogrModelMixin
from dlogr.exceptions import DlogrImproperlyConfigured


class Fixture1(DlogrModelMixin):
    id = 'fixture1_id'
    other_field = 'fixture1_other_field'

    def __str__(self):
        return 'Human identifier'

    def __repr__(self):
        return self.__str__()


class Fixture2(DlogrModelMixin):
    DLOGR_IDENTIFIER_FIELD = 'uuid'
    DLOGR_HUMAN_IDENTIFIER_FIELD = 'other_field'

    id = 'fixture2_id'
    uuid = 'fixture2_uuid'
    other_field = 'fixture2_other_field'

    def __str__(self):
        return 'Human identifier'

    def __repr__(self):
        return self.__str__()


@freeze_time(datetime(2016, 1, 1, 12, 12, 12))
@mock.patch('dlogr.clients.requests')
class DlogrClientListTestCase(unittest.TestCase):
    def setUp(self):
        super(DlogrClientListTestCase, self).setUp()
        os.environ['DLOGR_URL'] = 'http://api.dlogr.com'
        os.environ['DLOGR_ACCESS_KEY'] = 'my-cool-access-key'
        os.environ['DLOGR_ENABLED'] = 'True'
        os.environ['DLOGR_ASYNC'] = 'False'

    def tearDown(self):
        super(DlogrClientListTestCase, self).tearDown()
        os.environ.pop('DLOGR_URL', None)
        os.environ.pop('DLOGR_ACCESS_KEY', None)
        os.environ.pop('DLOGR_ENABLED', None)
        os.environ.pop('DLOGR_ASYNC', None)

    def test_fixture1_common(self, requests_patched):
        f1 = Fixture1()
        f1.dlogr_send('Here comes the message')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={u'Authorization': 'Token my-cool-access-key', 'user-agent': mock.ANY},
            params=None,
            verify=mock.ANY,
            data={
                'human_identifier': 'Human identifier',
                'timestamp': '2016-01-01T12:12:12',
                'message': 'Here comes the message',
                'object_type': 'tests.test_mixins.Fixture1',
                'object_id': 'fixture1_id'
            },
        )

    def test_fixture1_custom_date(self, requests_patched):
        f1 = Fixture1()
        f1.dlogr_send('Here comes the message', timestamp=datetime(2016, 7, 5, 15, 15, 15))

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={u'Authorization': 'Token my-cool-access-key', 'user-agent': mock.ANY},
            params=None,
            verify=mock.ANY,
            data={
                'human_identifier': 'Human identifier',
                'timestamp': '2016-07-05T15:15:15',
                'message': 'Here comes the message',
                'object_type': 'tests.test_mixins.Fixture1',
                'object_id': 'fixture1_id'
            },
        )

    def test_fixture2_common(self, requests_patched):
        f2 = Fixture2()
        f2.dlogr_send('Here comes the message')

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={u'Authorization': 'Token my-cool-access-key', 'user-agent': mock.ANY},
            params=None,
            verify=mock.ANY,
            data={
                'human_identifier': 'fixture2_other_field',
                'timestamp': '2016-01-01T12:12:12',
                'message': 'Here comes the message',
                'object_type': 'tests.test_mixins.Fixture2',
                'object_id': 'fixture2_uuid'
            },
        )

    def test_fixture2_custom_date(self, requests_patched):
        f2 = Fixture2()
        f2.dlogr_send('Here comes the message', timestamp=datetime(2016, 7, 5, 15, 15, 15))

        requests_patched.post.assert_called_once_with(
            'http://api.dlogr.com/api/events',
            auth=None,
            headers={u'Authorization': 'Token my-cool-access-key', 'user-agent': mock.ANY},
            params=None,
            verify=mock.ANY,
            data={
                'human_identifier': 'fixture2_other_field',
                'timestamp': '2016-07-05T15:15:15',
                'message': 'Here comes the message',
                'object_type': 'tests.test_mixins.Fixture2',
                'object_id': 'fixture2_uuid'
            },
        )

    def test_missing_DLOGR_URL_env_var(self, requests_patched):
        os.environ.pop('DLOGR_URL', None)
        f1 = Fixture1()

        with self.assertRaises(DlogrImproperlyConfigured) as context:
            f1.dlogr_send('Here comes the message')
        self.assertEquals(
            '{}'.format(context.exception),
            'In order to use Dlogr you *must* set both DLOGR_URL and DLOGR_ACCESS_KEY env vars.'
        )

    def test_missing_DLOGR_ACCESS_KEY_env_var(self, requests_patched):
        os.environ.pop('DLOGR_ACCESS_KEY', None)
        f1 = Fixture1()

        with self.assertRaises(DlogrImproperlyConfigured) as context:
            f1.dlogr_send('Here comes the message')
        self.assertEquals(
            '{}'.format(context.exception),
            'In order to use Dlogr you *must* set both DLOGR_URL and DLOGR_ACCESS_KEY env vars.'
        )

    def test_dlogr_disabled(self, requests_patched):
        os.environ['DLOGR_ENABLED'] = 'False'

        f1 = Fixture1()
        f1.dlogr_send('Here comes the message')
        self.assertFalse(requests_patched.post.called)
