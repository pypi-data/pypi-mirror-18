from __future__ import unicode_literals

import requests
from requests.auth import AuthBase


class FailedLogin(Exception):
    pass


class InvalidConfiguration(Exception):
    pass


class RocketAuth(AuthBase):
    def __init__(self, host, username=None, password=None, token=None, user_id=None):
        self.token = token
        self.user_id = user_id

        self._check_parameters(host, username, password, token, user_id)

        if username and password:
            self._do_login(host, username, password)

    @staticmethod
    def _check_parameters(host, username, password, token, user_id):
        try:
            assert host
            assert username and password or token and user_id

        except AssertionError:
            raise InvalidConfiguration('host and username/password or token/user_id')

    def _do_login(self, host, user, password):
        response = requests.post('{}/api/login'.format(host), data=dict(user=user, password=password))

        if response.status_code != 200:
            raise FailedLogin

        self._save_auth_headers(response)

    def _save_auth_headers(self, response):
        json = response.json()

        self.token = json['data']['authToken']
        self.user_id = json['data']['userId']

    def _set_auth_headers(self, request):
        request.headers['X-Auth-Token'] = self.token
        request.headers['X-User-Id'] = self.user_id

    def __call__(self, request):
        self._set_auth_headers(request)

        return request
