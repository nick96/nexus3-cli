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

    def test_download(self, repository_factory, nexus_client):
        repository = repository_factory(PypiHostedRepository)
        repository.upload_file('tests/fixtures/pypi/example-0.0.0.tar.gz')
        repository.download('packages/example/0.0.0/example-0.0.0.tar.gz', '/dev/null')

    def test_upload_whl(self, repository_factory):
        repository = repository_factory(PypiHostedRepository)
        repository.upload_file('tests/fixtures/pypi/empty-0.1.0-py3-none-any.whl')

    def test_download_whl(self, repository_factory, nexus_client):
        repository = repository_factory(PypiHostedRepository)
        repository.download('packages/empty/0.1.0/empty-0.1.0-py3-none-any.whl', '/dev/null')

    def test_delete(self, nexus_client, repository_factory):
        repository = repository_factory(PypiHostedRepository)
        nexus_client.repositories.delete(repository.name)
