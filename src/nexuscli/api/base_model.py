from typing import Optional

import nexuscli  # noqa: F401; for mypy and to avoid circular dependency


# When Python 3.6 is deprecated, switch to data class?
class BaseModel:
    """
    Base class for Nexus 3 server objects.

    Args:
        client (): the client instance that
            will be used to perform operations against the Nexus 3 service. You
            must provide this at instantiation or set it before calling any
            methods that require connectivity to Nexus.
    """
    def __init__(self, client: Optional['nexuscli.nexus_client.NexusClient'], **kwargs):
        self._client: Optional['nexuscli.nexus_client.NexusClient'] = client
        self._raw = kwargs  # type: dict

    @property
    def configuration(self) -> dict:
        """
        The model representation as a transformed python dict suitable for converting to JSON and
        passing-through to the Nexus 3 API.
        """
        return self._raw
