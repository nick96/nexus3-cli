import itertools
import pathlib
import pytest
from semver import VersionInfo

from nexuscli import nexus_util
from nexuscli.api.repository import collection
from nexuscli.api.repository.base_models.repository import Repository, CLEANUP_SET_MIN_VERSION


@pytest.mark.parametrize('recipe', [x.RECIPE_NAME for x in collection.get_repository_classes()])
def test_list(recipe, x_artefacts, faker, mocker):
    """Ensure the method yields the `path` attribute of each element returned by list_raw()"""
    x_repository_path = faker.uri_path()
    x_list_raw = pytest.helpers.nexus_raw_response(x_artefacts)

    r = Repository(name='dummy', recipe=recipe)
    mocker.patch.object(r, 'list_raw', return_value=x_list_raw)

    artefacts = list(r.list(x_repository_path))

    assert artefacts == x_artefacts
    r.list_raw.assert_called_with(x_repository_path)


@pytest.mark.parametrize('recipe,version_policy', itertools.product(
    [x.RECIPE_NAME for x in collection.get_repository_classes()], [
        (None, lambda x: [x]),
        (CLEANUP_SET_MIN_VERSION, lambda x: [x]),
        (VersionInfo(0, 0, 0), lambda x: x)]))
def test_cleanup_policy(recipe, version_policy, faker, mocker):
    """
    From CLEANUP_SET_MIN_VERSION, Nexus takes a set of policy names instead of a single policy.
    Ensure the method returns the right type according to the version.
    https://github.com/thiagofigueiro/nexus3-cli/issues/77
    """
    version, x_policy = version_policy
    policy = faker.word()
    nexus_http = mocker.Mock()
    nexus_http.server_version = version

    repository = Repository(nexus_http, name='dummy', cleanup_policy=policy, recipe=recipe)

    assert repository.cleanup_policy == x_policy(policy)


@pytest.mark.parametrize('recipe, recurse, flatten', itertools.product(
    [x.RECIPE_NAME for x in collection.get_classes_by_type('group')],  # format
    [True, False],       # recurse
    [True, False]))      # flatten
def test_upload_directory(recipe, recurse, flatten, x_artefacts, mocker, faker):
    """
    Ensure the method calls upload_file with parameters based on the quantity
    of files in a given directory.
    """
    src_dir = pathlib.Path(nexus_util.REMOTE_PATH_SEPARATOR.join(faker.words()))
    dst_dir = pathlib.Path(nexus_util.REMOTE_PATH_SEPARATOR.join(faker.words()))

    util = mocker.patch('nexuscli.api.repository.base_models.repository.util')
    util.get_files.return_value = [src_dir.joinpath(x[1:]) for x in x_artefacts]

    r = Repository(name='dummy', recipe=recipe)
    r.upload_file = mocker.Mock()

    x_upload_file_calls = [
        mocker.call(x, r._upload_dst_path(src_dir, x, dst_dir, flatten))
        for x in util.get_files.return_value
    ]

    count = r.upload_directory(src_dir, dst_dir, recurse=recurse, flatten=flatten)

    assert count == len(util.get_files.return_value)
    util.get_files.assert_called_with(src_dir, recurse)
    r.upload_file.assert_has_calls(x_upload_file_calls)


@pytest.mark.parametrize('strict', [True, False])
def test_configuration(strict, faker):
    """Ensure the property returns the attributes required by Nexus"""
    x_name = faker.word()
    x_cleanup_policy = faker.word()
    x_blob_store_name = faker.word()

    kwargs = {
        'cleanup_policy': x_cleanup_policy,
        'blob_store_name': x_blob_store_name,
        'strict_content_type_validation': strict,
    }

    repo = Repository(name=x_name,  **kwargs)
    configuration = repo.configuration
    attributes = configuration['attributes']

    assert configuration['name'] == x_name
    assert configuration['recipeName'] == 'None-None'  # base class has no name
    assert attributes['cleanup']['policyName'] == [x_cleanup_policy]
    assert attributes['storage']['blobStoreName'] == x_blob_store_name
    assert attributes['storage']['strictContentTypeValidation'] == strict


@pytest.mark.parametrize('recipe', [x.RECIPE_NAME for x in collection.get_repository_classes()])
def test_delete(recipe, x_artefacts, faker, nexus_mock_http, response_mock, mocker):
    """
    Given a repository_path and a response from the service, ensure that the
    method deletes the expected artefacts.
    """
    x_path = faker.uri_path()
    # Use list instead of generator so we can inspect contents
    x_list_raw = [x for x in pytest.helpers.nexus_raw_response(x_artefacts)]
    nexus_mock_http.delete = mocker.Mock(return_value=response_mock(204, 'All OK'))

    r = Repository(nexus_http=nexus_mock_http, name='dummy', recipe=recipe)
    mocker.patch.object(r, 'list_raw', return_value=x_list_raw)

    delete_count = r.delete(x_path)

    assert delete_count == len(x_artefacts)
    r.list_raw.assert_called_with(x_path)
