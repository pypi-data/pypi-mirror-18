import json
import logging
from urlparse import urlparse
import requests
import cnrclient
from cnrclient.discovery import ishosted, discover_sources


logger = logging.getLogger(__name__)
DEFAULT_REGISTRY = 'http://localhost:5000'
DEFAULT_PREFIX = ""


class CnrClient(object):
    def __init__(self, endpoint=DEFAULT_REGISTRY, api_prefix=DEFAULT_PREFIX, auth=None):
        if endpoint is None:
            endpoint = DEFAULT_REGISTRY
        if api_prefix:
            endpoint = endpoint + api_prefix

        self.auth = auth
        self.endpoint = urlparse(endpoint)

        self._headers = {'Content-Type': 'application/json',
                         'User-Agent': "cnrpy-cli: %s" % cnrclient.__version__}

    def _url(self, path):
        return self.endpoint.geturl() + path

    def auth_token(self):
        """ return the Authorization bearer """
        return self.auth

    @property
    def headers(self):
        token = self.auth_token()
        headers = {}
        headers.update(self._headers)
        if token is not None:
            headers['Authorization'] = token
        return headers

    def version(self):
        path = "/version"
        resp = requests.get(self._url(path), headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def pull(self, name, version, media_type):
        if ishosted(name):
            sources = discover_sources(name, version, media_type)
            path = sources[0]
        else:
            organization, name = name.split("/")
            path = self._url("/api/v1/packages/%s/%s/%s/%s/pull" % (organization, name, version, media_type))
        resp = requests.get(path, headers=self.headers)
        resp.raise_for_status()
        return resp.content

    def list_packages(self, user=None, organization=None):
        path = "/api/v1/packages"
        params = {}
        if user:
            params['username'] = user
        if organization:
            params["organization"] = organization
        resp = requests.get(self._url(path), params=params, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def push(self, name, body, force=False):
        organization, pname = name.split("/")
        body['name'] = pname
        body['organization'] = organization
        body['package'] = name
        path = "/api/v1/packages/%s/%s" % (organization, pname)
        resp = requests.post(self._url(path),
                             params={"force": str(force).lower()},
                             data=json.dumps(body), headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def delete_package(self, name, version, media_type):
        organization, name = name.split("/")
        path = "/api/v1/packages/%s/%s/%s/%s" % (organization, name, version, media_type)
        resp = requests.delete(self._url(path), headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def _crud_channel(self, name, channel='', action='get'):
        if channel is None:
            channel = ''
        path = "/api/v1/packages/%s/channels/%s" % (name, channel)
        resp = getattr(requests, action)(self._url(path), params={}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def show_channels(self, name, channel=None):
        return self._crud_channel(name, channel)

    def create_channel(self, name, channel):
        return self._crud_channel(name, channel, 'post')

    def delete_channel(self, name, channel):
        return self._crud_channel(name, channel, 'delete')

    def create_channel_release(self, name, channel, release):
        path = "%s/%s" % (channel, release)
        return self._crud_channel(name, path, 'post')

    def delete_channel_release(self, name, channel, release):
        path = "%s/%s" % (channel, release)
        return self._crud_channel(name, path, 'delete')
