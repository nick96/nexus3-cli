import pytest
from nexuscli.api.blobstore import BlobstoreCollection


@pytest.fixture
def blobstore_collection(nexus_client) -> BlobstoreCollection:
    """An instance of :py:class:`BlobstoreCollection`"""
    return BlobstoreCollection(nexus_http=nexus_client.http)
