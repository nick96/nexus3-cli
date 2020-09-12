import json
import pathlib
import pytest

from nexuscli.api import repository


@pytest.fixture
def repository_collection(nexus_mock_http):
    """A RepositoryCollection with the nexus_client mocked"""
    fixture = repository.RepositoryCollection(nexus_http=nexus_mock_http)
    return fixture


@pytest.helpers.register
def default_repos():
    default_repos_path = pathlib.Path('tests/fixtures/default-repos')

    for config_file in default_repos_path.glob('*.json'):
        with config_file.open() as fh:
            config = json.load(fh)
        yield pytest.param(config, id=config_file.name)


@pytest.helpers.register
def compare_dict(d1, d2):
    """
    Compares dictionaries. Shamelessly
    borrowed from http://stackoverflow.com/a/18860653

    :param d2: dictionary to compare this one against
    :type d2: dict
    :return: tuple of entries that were: added, removed, modified, equal
    :rtype: tuple
    """
    self_keys = set(d1.keys())
    d_keys = set(d2.keys())
    intersect_keys = self_keys.intersection(d_keys)
    added = self_keys - d_keys
    removed = d_keys - self_keys
    modified = {
        o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]
    }
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same
