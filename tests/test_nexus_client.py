# -*- coding: utf-8 -*-
import pytest
import requests

import nexuscli
from nexuscli.nexus_client import NexusClient
from nexuscli.nexus_config import DEFAULTS, NexusConfig


def test_repositories(mocker):
    """
    Ensure that the class fetches repositories on instantiation
    """
    mocker.patch('nexuscli.nexus_client.RepositoryCollection')

    client = NexusClient()

    nexuscli.nexus_client.RepositoryCollection.assert_called()
    client.repositories.refresh.assert_called_once()


@pytest.mark.parametrize(
    'url,expected_base', [
        ('http://localhost:8081', 'http://localhost:8081/'),
        ('http://localhost:8081/', 'http://localhost:8081/'),
        ('http://localhost:8081/nexus', 'http://localhost:8081/nexus/'),
        ('http://localhost:8081/nexus/', 'http://localhost:8081/nexus/'),
    ]
)
def test_nexus_context_path(url, expected_base, mocker):
    """
    Check that the nexus context (URL prefix) is taken into account
    """
    class MockResponse:

        def __init__(self):
            self.status_code = 200

        def json(self):
            return '{}'

    mocker.patch('requests.request', return_value=MockResponse())

    NexusClient(NexusConfig(url=url))
    requests.request.assert_called_once_with(
        auth=(DEFAULTS['username'], DEFAULTS['password']), method='get',
        stream=True, url=(expected_base + 'service/rest/v1/repositories'),
        verify=True)
