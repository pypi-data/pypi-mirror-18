import logging
from typing import Any, Dict, List, Optional
from urllib.parse import quote as urlquote

import requests

logger = logging.getLogger('wobble')


def _normalize_app_id(app_id: str) -> str:
    """Return the normalized app id."""
    return urlquote('/' + app_id.strip('/'))


class MarathonClient:
    def __init__(self, host: str, token: Optional[str] = None):
        """
        Simple marathon api client, see the main docs for endpoint details

        https://mesosphere.github.io/marathon/docs/rest-api.html

        :param host: Marathon host url, this should include the context root.
        For marathon itself, there isn't likely a context root - however if
        running against DCOS, it will be something like /service/marathon
        :param token: If authentication is required, the token.
        """
        self._host = host.rstrip('/') + '/v2'
        self._session = requests.Session()
        if token:
            # Not sure why they don't use the standard "Bearer <token>"
            self._session.headers.update({
                'Authorization': 'token={}'.format(token),
            })

    def apps(self) -> List[Dict[str, Any]]:
        """Gets the list of applications"""
        return self._req('GET', '/apps').json()

    def deployments(self) -> List[Dict[str, Any]]:
        """Gets the list of active deployments"""
        return self._req('GET', '/deployments').json()

    def deploy(self, marathon_json: Dict[str, Any]) -> Dict[str, Any]:
        """Deploys an application, if it is not already created it
        will be - otherwise the existing application is updated.

        TODO: enable forcing if we decide we need it. Though it
        is likely less necessary since we are killing hung deployments
        automatically with wobble.
        """
        app_id = marathon_json['id']
        return self._req('PUT', '/apps' + _normalize_app_id(app_id),
                         json=marathon_json).json()

    def deploying(self, deploy_id: str) -> bool:
        """Check if the deployment id is in the deployment queue"""
        return any(x for x in self.deployments() if x['id'] == deploy_id)

    def kill_deployment(self, deploy_id: str) -> Dict[str, str]:
        """Kill a specific deployment"""
        return self._req('DELETE', '/deployments/' + deploy_id).json()

    def events(self) -> requests.Response:
        """Connect to the event stream, to consume you will need
        to use iter_lines"""
        return self._req('GET', '/events', stream=True,
                         headers={'Accept': 'text/event-stream'},
                         timeout=(3.05, None))

    def _req(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        Very thin wrapper around the requests call, the only
        difference is all calls are checked for a successful
        status before returning the http response.

        :param method: HTTP Method string
        :param path: Path within the marathon service.
        :param kwargs:
        :return: Decoded json response
        """
        r = self._session.request(method, self._host + path, **kwargs)
        r.raise_for_status()
        return r
