import json

from nexuscli import exception
from nexuscli.cli import nexus_cli


def test_active(cli_runner, mocker, nexus_mock_client, faker):
    """Test that the command calls the API and handles response correctly"""
    x_active = faker.words(unique=True)
    nexus_mock_client.security_realms.active = x_active
    mocker.patch('nexuscli.cli.util.get_client', return_value=nexus_mock_client)

    cmd = 'security realm active'
    result = cli_runner.invoke(nexus_cli, cmd, catch_exceptions=False)

    assert result.exit_code == exception.CliReturnCode.SUCCESS.value
    assert result.output == json.dumps(x_active) + '\n'


def test_available(cli_runner, mocker, nexus_mock_client, faker):
    """Test that the command calls the API and handles response correctly"""
    x_available = faker.words(unique=True)
    # nexus_mock_client._security_realms = mocker.Mock()
    nexus_mock_client.security_realms.list = x_available
    mocker.patch('nexuscli.cli.util.get_client', return_value=nexus_mock_client)

    cmd = 'security realm available --json'
    result = cli_runner.invoke(nexus_cli, cmd, catch_exceptions=False)

    assert result.exit_code == exception.CliReturnCode.SUCCESS.value
    assert result.output == json.dumps(x_available) + '\n'


def test_activate(cli_runner, mocker, nexus_mock_client, faker):
    """Test that the command calls the API with the given user parameter"""
    x_realm_id = faker.pystr()
    nexus_mock_client.security_realms.activate = mocker.Mock(return_value=x_realm_id)
    mocker.patch('nexuscli.cli.util.get_client', return_value=nexus_mock_client)

    cmd = f'security realm activate {x_realm_id}'
    result = cli_runner.invoke(nexus_cli, cmd, catch_exceptions=False)

    nexus_mock_client.security_realms.activate.assert_called_with(x_realm_id)
    assert result.exit_code == exception.CliReturnCode.SUCCESS.value
    assert result.output == ''
