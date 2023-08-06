from __future__ import unicode_literals

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)

from .resources import RESOURCE_MAPPING
from .auth import RocketAuth


class RocketChatClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(RocketChatClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['auth'] = RocketAuth(api_params.get('host'),
                                    api_params.get('username'),
                                    api_params.get('password'),
                                    api_params.get('token'),
                                    api_params.get('user_id'))

        return params

    def get_api_root(self, api_params):
        return '{}/api'.format(api_params.get('host', 'http://localhost'))


RocketChat = generate_wrapper_from_adapter(RocketChatClientAdapter)
