from __future__ import unicode_literals

import pytest
import requests_mock

from tapioca_rocketchat import RocketChat
from tapioca_rocketchat.auth import InvalidConfiguration, FailedLogin

AUTH_RESOURCE = 'http://localhost.com/api/login'
AUTH_RESPONSE = {'status': 'success', 'data': {'authToken': 'authToken', 'userId': 'userId'}}
AUTH_HEADERS = {'X-Auth-Token': 'authToken', 'X-User-Id': 'userId'}


@pytest.fixture
def client():
    return RocketChat(host='http://localhost.com', username='user', password='password')


@pytest.fixture
def client_token():
    return RocketChat(host='http://localhost.com', token='authToken', user_id='userId')


def test_should_hit_version_resource(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.get('http://localhost.com/api/version', request_headers=AUTH_HEADERS)

        response = client.version().get()

        assert response._response.status_code == 200


def test_should_login_with_correct_parameters(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        response = client.logon().post(data={'user': 'user', 'password': 'password'})

        assert response._response.status_code == 200


def test_should_join_a_room(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.post('http://localhost.com/api/rooms/room/join', request_headers=AUTH_HEADERS)

        response = client.join(room='room').post()

        assert response._response.status_code == 200


def test_should_raised_exception_when_logging_failed(client):
    with pytest.raises(FailedLogin):
        with requests_mock.Mocker() as m:
            m.post(AUTH_RESOURCE, json={}, status_code=401)

            m.post('http://localhost.com/api/rooms/room/join', request_headers=AUTH_HEADERS)

            response = client.join(room='room').post()

            assert response._response.status_code == 200


def test_should_leave_a_room(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.post('http://localhost.com/api/rooms/room/leave', request_headers=AUTH_HEADERS)

        response = client.leave(room='room').post()

        assert response._response.status_code == 200


def test_should_get_all_messages_of_a_room(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.get('http://localhost.com/api/rooms/room/messages', request_headers=AUTH_HEADERS)

        response = client.messages(room='room').get()

        assert response._response.status_code == 200


def test_should_send_a_message_to_a_room(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.post('http://localhost.com/api/rooms/room/send', status_code=201, request_headers=AUTH_HEADERS)

        response = client.send(room='room').post(data={'msg': 'msg'})

        assert response._response.status_code == 201


def test_should_create_a_channel(client):
    with requests_mock.Mocker() as m:
        m.post(AUTH_RESOURCE, json=AUTH_RESPONSE)

        m.post('http://localhost.com/api/v1/channels.create', status_code=201, request_headers=AUTH_HEADERS)

        response = client.channel().post(data={'name': 'channelname'})

        assert response._response.status_code == 201


def test_should_get_version_with_token(client_token):
    with requests_mock.Mocker() as m:
        m.get('http://localhost.com/api/version', status_code=200, request_headers=AUTH_HEADERS)

        response = client_token.version().get()

        assert response._response.status_code == 200


def test_should_raise_exception_when_missing_parameters():
    with pytest.raises(InvalidConfiguration):
        client = RocketChat()

        client.version().get()
