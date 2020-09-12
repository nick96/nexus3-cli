import json
import pytest

from nexuscli.cli import nexus_cli


@pytest.mark.xfail('https://gitlab.com/thiagocsf/nexus3-cli/-/issues/18')
@pytest.mark.integration
@pytest.mark.xfail(reason='https://gitlab.com/thiagocsf/nexus3-cli/-/issues/18')
def test_cleanup_policy(cli_runner, faker):
    """Ensure the command creates a new policy and that is shows on the list"""
    x_name = faker.pystr()
    # CLI accepts days, Nexus stores seconds
    downloaded = faker.random_int(1, 365)
    x_downloaded = str(downloaded * 86400)
    updated = faker.random_int(1, 365)
    x_updated = str(updated * 86400)

    create_command = (f'cleanup-policy create {x_name} --format all '
                      f'--downloaded={downloaded} --updated={updated}')
    list_command = 'cleanup-policy list'
    show_command = f'cleanup-policy show {x_name}'

    create_result = cli_runner.invoke(nexus_cli, create_command, catch_exceptions=False)
    list_result = cli_runner.invoke(nexus_cli, list_command, catch_exceptions=False)
    show_result = cli_runner.invoke(nexus_cli, show_command, catch_exceptions=False)
    policy = json.loads(show_result.output)

    assert create_result.exit_code == 0
    assert create_result.output == ''
    assert list_result.exit_code == 0
    assert x_name in list_result.output
    assert x_name == policy['name']
    assert x_downloaded == policy['criteria']['lastDownloaded']
    assert x_updated == policy['criteria']['lastBlobUpdated']
    assert 'ALL_FORMATS' == policy['format']
