import json

from ereuse_devicehub.exceptions import InnerRequestError
from eve.methods.delete import deleteitem_internal
from eve.methods.patch import patch_internal
from eve.methods.post import post_internal
from flask import request, current_app


def execute_post(resource: str, payload: dict, skip_validation=False):
    response = post_internal(resource, payload, skip_validation)
    if response[3] != 201:  # statusCode
        raise InnerRequestError(response[3], response[0])
    return response[0]  # Actual data


def execute_get(url: str, token: str = None):
    http_authorization = request.headers.environ['HTTP_AUTHORIZATION'] if token is None else 'Basic ' + token
    response = current_app.test_client().get(url, environ_base={'HTTP_AUTHORIZATION': http_authorization})
    data = json.loads(response.data.decode())  # It is useless to use json_util
    if response._status_code != 200:
        data['url'] = url
        raise InnerRequestError(response._status_code, data)
    else:
        return data


def execute_patch(resource: str, payload: dict, identifier):
    payload['_id'] = str(identifier)
    response = patch_internal(resource, payload, False, False, **{'_id': str(identifier)})
    if response[3] != 200:  # statusCode
        raise InnerRequestError(response[3], response[0])
    return response[0]


def execute_delete(resource: str, identifier):
    _, _, _, status = deleteitem_internal(resource, **{'_id': str(identifier)})
    if status != 204:
        raise InnerRequestError(status, {})
