# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import sys

from requests.exceptions import RequestException
import requests

from dlogr import __version__
from dlogr.exceptions import DlogrAPIError


class DlogrRequestMixin(object):
    def __init__(self, base_api_url, auth_credentials, auth_token):
        self.base_api_url = base_api_url
        self.auth_credentials = auth_credentials
        self.auth_token = auth_token

    def get_full_endpoint(self, path):
        return '{}{}'.format(self.base_api_url, path)

    def _request(self, requests_method, url, data=None, params=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cert_path = os.path.join(current_dir, 'gd_bundle-g2-g1.crt')

        auth = None
        headers = {
            'user-agent': 'dlogr/{} python/{}'.format(__version__, sys.version.split()[0]),
        }

        if self.auth_token:
            headers['Authorization'] = 'Token {}'.format(self.auth_token)
        elif self.auth_credentials:
            auth = self.auth_credentials

        try:
            return requests_method(url, auth=auth, headers=headers, data=data, params=params, verify=cert_path)
        except RequestException as e:
            raise DlogrAPIError('{}'.format(e))


class DlogrBaseResource(DlogrRequestMixin):
    endpoint = ''  # Must be set on children classes.

    def get_full_list_endpoint(self):
        return self.get_full_endpoint(self.endpoint)

    def get_full_details_endpoint(self, identifier):
        return '{}/{}'.format(self.get_full_list_endpoint(), identifier)

    def list(self, **params):
        '''
        Fetches a list of resources on API. Use params for endpoint query params (pagination, filtering, ordering, etc)
        Example of params:
        - limit, offset (for pagination - defaults to 30 and 0)
        - object_type, object_id, human_identifier (for filtering)
        - fields, exclude (for reducing API response payload)
        - ordering (for... guess what?)
        '''
        params.setdefault('limit', 30)
        params.setdefault('offset', 0)
        return self._request(requests.get, self.get_full_list_endpoint(), params=params)

    def create(self, **data):
        return self._request(requests.post, self.get_full_list_endpoint(), data=data)

    def retrieve(self, identifier):
        return self._request(requests.get, self.get_full_details_endpoint(identifier))

    def update(self, identifier, **data):
        return self._request(requests.patch, self.get_full_details_endpoint(identifier), data=data)

    def delete(self, identifier):
        return self._request(requests.delete, self.get_full_details_endpoint(identifier))


class DlogrEventResource(DlogrBaseResource):
    endpoint = '/api/events'


class DlogrCustomerResource(DlogrBaseResource):
    endpoint = '/api/customers'


class DlogrAuthResource(DlogrRequestMixin):
    def login(self, email, password):
        data = {
            'email': email,
            'password': password,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/login'), data=data)

    def verify_account(self, token):
        data = {
            'token': token,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/verify-account'), data=data)

    def reset_password(self, email):
        data = {
            'email': email,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/reset-password'), data=data)

    def change_password(self, new_password, email=None, password=None, reset_token=None):
        data = {
            'new_password': new_password,
            'email': email,
            'password': password,
            'reset_token': reset_token,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/change-password'), data=data)


class DlogrClient(object):
    def __init__(self, base_api_url, auth_credentials=None, auth_token=None):
        self.base_api_url = base_api_url
        self.auth_credentials = auth_credentials
        self.auth_token = auth_token

    @property
    def base_resource_parameters(self):
        return {
            'base_api_url': self.base_api_url,
            'auth_credentials': self.auth_credentials,
            'auth_token': self.auth_token,
        }

    @property
    def Event(self):
        return DlogrEventResource(**self.base_resource_parameters)

    @property
    def Customer(self):
        return DlogrCustomerResource(**self.base_resource_parameters)

    @property
    def Auth(self):
        return DlogrAuthResource(**self.base_resource_parameters)
