import pytest

from nexuscli.api.repository.model import MavenHostedRepository


@pytest.mark.xfail(reason='Not implemented', strict=True)
def test_upload_error(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(MavenHostedRepository)
