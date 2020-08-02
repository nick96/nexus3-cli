import json
import pytest

from nexuscli import exception
from nexuscli.cli import nexus_cli


@pytest.mark.integration
def test_list(cli_runner):
    """Test that the command has valid json output"""
    cmd = 'task list --json'
    result = cli_runner.invoke(nexus_cli, cmd)
    content = json.loads(result.output)

    assert result.exit_code == exception.CliReturnCode.SUCCESS.value
    assert isinstance(content['items'], list)


@pytest.mark.integration
def test_show_error(cli_runner):
    """Ensure the command raises an exception for task id not found"""
    cmd = 'task show some-bogus-id'
    result = cli_runner.invoke(nexus_cli, cmd)

    assert result.exit_code == exception.CliReturnCode.NOT_FOUND.value
    assert 'Error: some-bogus-id' in result.output
