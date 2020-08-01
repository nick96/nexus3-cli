import pytest

from nexuscli.api.repository.model import NpmHostedRepository


def test_upload_error(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(NpmHostedRepository)


@pytest.mark.integration
@pytest.mark.incremental
class TestNpmHostedRepository:
    def test_create(self, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        repository.nexus_client.repositories.create(repository)

    def test_upload(self, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        repository.upload_file('tests/fixtures/npm/example-0.0.0.tgz')

    def test_delete(self, repository_factory):
        repository = repository_factory(NpmHostedRepository)
        repository.nexus_client.repositories.delete(repository.name)
