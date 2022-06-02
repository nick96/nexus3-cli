import pytest

from nexuscli import exception
from nexuscli.nexus_client import NexusClient


def test_run_script_groovy_disabled(nexus_mock_http, faker, mocker):
    mocker.patch('nexuscli.nexus_config.NexusConfig.groovy_enabled',
                 new_callable=mocker.PropertyMock, return_value=False)
    mocker.patch.object(NexusClient, 'security_realms', new_callabe=mocker.PropertyMock)

    client = NexusClient()

    with pytest.raises(exception.FeatureNotImplemented):
        client.scripts.run_script(faker.file_name())
