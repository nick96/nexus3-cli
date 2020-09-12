import pytest

from nexuscli import exception
from nexuscli.api.repository.model import NpmHostedRepository


def test_upload_error(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(NpmHostedRepository)


@pytest.mark.integration
@pytest.mark.incremental
class TestNpmHostedRepository:
    def test_create(self, nexus_client, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        nexus_client.repositories.create(repository)

    def test_upload(self, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        repository.upload_file('tests/fixtures/npm/example-0.0.0.tgz')

    def test_delete(self, nexus_client, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        nexus_client.repositories.delete(repository.name)

    def test_get(self, nexus_client, repository_factory):
        """Ensure it was deleted"""
        repository = repository_factory(NpmHostedRepository)
        with pytest.raises(exception.NexusClientInvalidRepository):
            nexus_client.repositories.get_by_name(repository.name)
