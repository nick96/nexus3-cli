from typing import List, Optional

import nexuscli


class BaseCollection:
    """
    A base collection class that contains a Nexus 3 client.

    Args:
        client: the client instance that will be used to perform operations against the Nexus 3
        service. You must provide this at instantiation or set it before calling any methods that
        require connectivity to Nexus.
    """
    def __init__(self, client: 'nexuscli.nexus_client.NexusClient' = None):
        self._client = client
        self._list: Optional[List[dict]] = None

    @property
    def list(self) -> List[dict]:
        """Cached version of :py:meth:`raw_list`. Use :py:meth:`reset` to refresh."""
        if self._list is None:
            self._list = self.raw_list()
        return self._list

    def raw_list(self) -> List[dict]:
        raise NotImplementedError

    def reset(self) -> None:
        """
        Clears the cached collection and causes the next call to :py:meth:`list` to reload the
        response from the Nexus server.
        """
        self._list = None

    def _service_get(self, endpoint: str, api_version: Optional[str] = None):
        """Most implementations of :py:meth:`raw_list` will use something like this"""
        if self._client is None:
            raise AttributeError('Define a client before using this method')

        service_url = None
        if api_version is not None:
            service_url = self._client.rest_url + api_version + '/'
        resp = self._client.http_get(endpoint, service_url=service_url)

        if resp.status_code != 200:
            raise nexuscli.exception.NexusClientAPIError(resp.content)

        return resp.json()
