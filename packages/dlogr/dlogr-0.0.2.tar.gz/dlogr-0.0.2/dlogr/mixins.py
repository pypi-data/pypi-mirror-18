# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import os

from dlogr.clients import DlogrClient
from dlogr.exceptions import DlogrImproperlyConfigured
from dlogr.utils import env_to_bool


DLOGR_ASYNC = env_to_bool('DLOGR_ASYNC', default=None)
if DLOGR_ASYNC is None:
    try:
        from celery import shared_task  # noqa
        DLOGR_ASYNC = True
    except ImportError:
        DLOGR_ASYNC = False


def create_event(base_api_url, auth_token, message, timestamp, object_id, object_type, human_identifier):
    client = DlogrClient(base_api_url=base_api_url, auth_token=auth_token)
    return client.Event.create(
        message=message,
        timestamp=timestamp,
        object_id=object_id,
        object_type=object_type,
        human_identifier=human_identifier
    )


if DLOGR_ASYNC:
    from celery import shared_task  # noqa
    create_event = shared_task(create_event).delay


class DlogrModelMixin(object):
    DLOGR_IDENTIFIER_FIELD = 'id'
    DLOGR_HUMAN_IDENTIFIER_FIELD = None

    def _fully_qualified_object_path(self):
        return '{}.{}'.format(self.__class__.__module__, self.__class__.__name__)

    def dlogr_send(self, message, timestamp=None):
        if not env_to_bool('DLOGR_ENABLED', default=True):
            return

        if not timestamp:
            timestamp = datetime.utcnow()

        try:
            base_api_url = os.environ['DLOGR_URL']
            auth_token = os.environ['DLOGR_ACCESS_KEY']
        except KeyError:
            raise DlogrImproperlyConfigured(
                'In order to use Dlogr you *must* set both DLOGR_URL and DLOGR_ACCESS_KEY env vars.'
            )

        object_id = str(getattr(self, self.DLOGR_IDENTIFIER_FIELD))
        object_type = self._fully_qualified_object_path()
        timestamp = timestamp.isoformat()

        if self.DLOGR_HUMAN_IDENTIFIER_FIELD:
            human_identifier = getattr(self, self.DLOGR_HUMAN_IDENTIFIER_FIELD)
        else:
            human_identifier = '{}'.format(self)

        return create_event(base_api_url, auth_token, message, timestamp, object_id, object_type, human_identifier)
