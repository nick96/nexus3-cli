import pytest


@pytest.fixture
def x_artefacts(faker):
    """list with random count of artefact paths with random directory depth"""
    return [
        faker.file_path(
            depth=faker.random_int(2, 10)) for _ in range(faker.random_int(1, 20))
    ]
