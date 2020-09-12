import pytest

from nexuscli.api.repository.model import PypiHostedRepository


def test_upload_error(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(PypiHostedRepository)


@pytest.mark.integration
@pytest.mark.incremental
class TestPypiHostedRepository:
    def test_create(self, nexus_client, repository_factory):
        repository = repository_factory(PypiHostedRepository)
        nexus_client.repositories.create(repository)

    def test_upload(self, repository_factory):
        repository = repository_factory(PypiHostedRepository)
        repository.upload_file('tests/fixtures/pypi/example-0.0.0.tar.gz')

    def test_delete(self, nexus_client, repository_factory):
        repository = repository_factory(PypiHostedRepository)
        nexus_client.repositories.delete(repository.name)
