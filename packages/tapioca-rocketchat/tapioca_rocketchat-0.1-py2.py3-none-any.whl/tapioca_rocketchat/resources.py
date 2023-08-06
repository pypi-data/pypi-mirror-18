from __future__ import unicode_literals

RESOURCE_MAPPING = {
    'version': {
        'resource': '/version',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#obtaining-the-running-rocket-chat-version-via-rest-api',
        'methods': ['GET']
    },

    'logon': {
        'resource': '/login',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#logon',
        'methods': ['POST']
    },

    'logoff': {
        'resource': '/logout',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#logoff',
        'methods': ['POST']
    },

    'rooms': {
        'resource': '/publicRooms',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#get-list-of-public-rooms',
        'methods': ['GET']
    },

    'join': {
        'resource': '/rooms/{room}/join',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#join-a-room',
        'methods': ['GET']
    },

    'leave': {
        'resource': '/rooms/{room}/leave',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#leave-a-room',
        'methods': ['POST']
    },

    'messages': {
        'resource': '/rooms/{room}/messages',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#get-all-messages-in-a-room',
        'methods': ['GET']
    },

    'send': {
        'resource': '/rooms/{room}/send',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#sending-a-message',
        'methods': ['POST']
    },

    'channel': {
        'resource': '/v1/channels.create',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#create-a-channel',
        'methods': ['POST']
    },

    'user': {
        'resource': '/v1/users.create',
        'docs': 'https://rocket.chat/docs/developer-guides/rest-api/#create-a-user',
        'methods': ['POST']
    },
}
