import pytest
import requests

from nexuscli.nexus_client import NexusClient
from nexuscli.nexus_config import DEFAULTS, NexusConfig


@pytest.mark.parametrize(
    'url,expected_base', [
        ('http://localhost:8081', 'http://localhost:8081/'),
        ('http://localhost:8081/', 'http://localhost:8081/'),
        ('http://localhost:8081/nexus', 'http://localhost:8081/nexus/'),
        ('http://localhost:8081/nexus/', 'http://localhost:8081/nexus/'),
    ]
)
def test_nexus_context_path(url, expected_base, mocker, faker):
    """
    Check that the nexus context (URL prefix) is taken into account
    """
    class MockResponse:

        def __init__(self):
            self.status_code = 200

        def json(self):
            return '{}'

    x_path = faker.uri_path()
    mocker.patch('requests.request', return_value=MockResponse())

    NexusClient(NexusConfig(url=url)).http.get(x_path)
    requests.request.assert_called_once_with(
        auth=(DEFAULTS['username'], DEFAULTS['password']), method='get',
        stream=True, url=f'{expected_base}service/rest/v1/{x_path}',
        verify=True)
