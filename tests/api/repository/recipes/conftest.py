import pytest

from nexuscli import exception


@pytest.fixture
def upload_file_ensure_raises_api_error(tmpdir, faker, mock_nexus_client):
    def fixture(repository_class):
        repository = repository_class(faker.word(), nexus_client=mock_nexus_client)
        # TODO: use the file_upload_args fixture
        src_file = tmpdir.join(faker.file_name()).ensure()

        with pytest.raises(exception.NexusClientAPIError):
            repository.upload_file(src_file, faker.file_path(), faker.file_name())

    return fixture
