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
