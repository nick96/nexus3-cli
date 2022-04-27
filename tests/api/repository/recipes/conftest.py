import pytest

from nexuscli import exception


@pytest.fixture
def repository_factory(nexus_client):
    def fixture(repository_class):
        repository = repository_class(nexus_client.http, name=repository_class.__name__)
        return repository

    return fixture


@pytest.fixture
def upload_file_ensure_raises_api_error(tmpdir, faker, nexus_mock_client):
    def fixture(repository_class):
        repository = repository_class(nexus_mock_client.http, name=faker.word())
        nexus_mock_client.http.request.return_value.status_code = 500
        # TODO: use the file_upload_args fixture
        src_file = tmpdir.join(faker.file_name()).ensure()
        with pytest.raises(exception.NexusClientAPIError):
            repository.upload_file(src_file, faker.file_path())

    return fixture
