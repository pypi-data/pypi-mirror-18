import json

from bravado.client import SwaggerClient


class APIClient(object):
    def __init__(self, url):
        self._client = SwaggerClient.from_url(url + '/swagger.json', config={
            'validate_swagger_spec': False,
            'use_models': False,
        })

    def __getattr__(self, item):
        if item == "_client":
            return super(APIClient, self).__getattr__(item)

        return MethodProxy(getattr(self._client, item))


class MethodProxy(object):
    def __init__(self, resource):
        self._resource = resource

    def __getattr__(self, item):
        if item == "_client":
            return super(MethodProxy, self).__getattr__(item)

        method = getattr(self._resource, item)

        def func(*args, **kwargs):
            http_feature = method(*args, **kwargs)
            return self._get_json_result(http_feature)

        return func

    @staticmethod
    def _get_json_result(http_feature, timeout=None):
        inner_response = http_feature.future.result(timeout=timeout)
        return json.loads(inner_response.text)
