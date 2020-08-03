import pytest

from nexuscli import exception
from nexuscli.api import util
from nexuscli.api.base_collection import BaseCollection


def test_with_min_version(nexus_mock_client):
    """
    Ensure the decorator:
    1. raises an exception when the server version is less than required
    2. runs the decorated method and returns its value when the server version is equal the
       required
    """
    min_version = nexus_mock_client._server_version.next_version('patch')

    @util.with_min_version(str(nexus_mock_client._server_version))
    def collection_method_good(self):
        return 1

    @util.with_min_version('0.0.0')
    def collection_method_alsogood(self):
        return 2

    @util.with_min_version(str(min_version))
    def collection_method_bad(self):
        pass

    collection = BaseCollection(client=nexus_mock_client)
    with pytest.raises(exception.NexusClientCapabilityUnsupported):
        collection_method_bad(collection)

    assert collection_method_good(collection) == 1
    assert collection_method_alsogood(collection) == 2
