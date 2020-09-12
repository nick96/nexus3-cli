import itertools
import pytest

from nexuscli.api.repository import collection


@pytest.mark.parametrize('class_,method_name', itertools.product(
    collection.get_classes_by_type(['proxy']), ['upload_file', 'upload_directory']))
def test_upload_file(class_, method_name, faker):
    """Ensure that no proxy repositories have the upload_file, upload_directory methods"""
    repo = class_(None, name='dummy', remote_url=faker.url())

    method = getattr(repo, method_name)
    with pytest.raises(NotImplementedError):
        method('dummy', 'dummy')


@pytest.mark.parametrize('repo_class, auto_block, negative_cache, auth_type', itertools.product(
    [x for x in collection.get_classes_by_type('proxy')],
    [True, False],  # auto_block
    [True, False],  # negative_cache
    [None, 'username'],  # auth_type
))
def test_configuration(repo_class, auto_block, negative_cache, auth_type, faker):
    """Ensure the property returns the attributes required/supported by Nexus"""
    x_remote_url = faker.url()
    x_content_max_age = faker.pyint()
    x_metadata_max_age = faker.pyint()
    x_negative_cache_ttl = faker.pyint()
    x_username = faker.user_name()
    x_password = faker.password()

    kwargs = {
        'auto_block': auto_block,
        'negative_cache_enabled': negative_cache,
        'remote_url': x_remote_url,
        'content_max_age': x_content_max_age,
        'metadata_max_age': x_metadata_max_age,
        'negative_cache_ttl': x_negative_cache_ttl,
        'remote_auth_type': auth_type,
        'remote_username': x_username,
        'remote_password': x_password,
    }

    repo = repo_class(name='dummy',  **kwargs)
    configuration = repo.configuration
    attributes = configuration['attributes']

    assert configuration['recipeName'] == repo._nexus_recipe_name
    assert attributes['httpclient']['connection']['autoBlock'] == auto_block
    assert attributes['proxy']['remoteUrl'] == x_remote_url
    assert attributes['proxy']['contentMaxAge'] == x_content_max_age
    assert attributes['proxy']['metadataMaxAge'] == x_metadata_max_age
    assert attributes['negativeCache']['enabled'] == negative_cache
    assert attributes['negativeCache']['timeToLive'] == x_negative_cache_ttl
    if auth_type == 'username':
        assert attributes['httpclient']['authentication']['type'] == auth_type
        assert attributes['httpclient']['authentication']['username'] == x_username
        assert attributes['httpclient']['authentication']['password'] == x_password
    else:
        assert attributes['httpclient'].get('authentication') is None
