import pytest

from nexuscli import exception
from nexuscli.api.blobstore import Blobstore


@pytest.mark.integration
def test_raw_list(blobstore_collection):
    assert len(blobstore_collection.raw_list()) > 0


@pytest.mark.integration
def test_get_by_name(blobstore_collection):
    x_configuration = {'name': 'default', 'path': 'default', 'softQuota': None, 'type': 'File'}
    b = blobstore_collection.get_by_name('default')

    assert isinstance(b, Blobstore)
    assert b.configuration == x_configuration


@pytest.mark.integration
def test_quota_status(blobstore_collection):
    x_status = {
        'isViolation': False,
        'message': 'Blob store default has no quota',
        'blobStoreName': 'default'}
    status = blobstore_collection.quota_status('default')

    assert status == x_status


@pytest.mark.integration
@pytest.mark.incremental
class TestBlobstore:
    name = 'some-name'
    path = '/tmp/some-path'

    def test_create(self, blobstore_collection):
        blobstore = Blobstore(name=self.name, path=self.path, type='file')
        blobstore_collection.create(blobstore)
        remote_blobstore = blobstore_collection.get_by_name(self.name)

        assert remote_blobstore.configuration == blobstore.configuration

    def test_delete(self, blobstore_collection):
        blobstore_collection.delete(self.name)

        with pytest.raises(exception.NotFound):
            blobstore_collection.get_by_name(self.name)

        with pytest.raises(exception.NexusClientAPIError):
            blobstore_collection.delete(self.name)
