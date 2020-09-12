import pytest
from nexuscli.api.repository.model import YumHostedRepository, YumProxyRepository


def test_upload_error(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(YumHostedRepository)


@pytest.mark.parametrize('class_', [YumHostedRepository, YumProxyRepository])
def test_configuration(class_, faker):
    x_depth = faker.pyint()

    # This will break once YumHosted starts validating unknown kwargs (remote_url is Proxy only)
    repo = class_(name='dummy', depth=x_depth, remote_url='http://dummy')

    assert repo.configuration['attributes']['yum']['repodataDepth'] == x_depth
