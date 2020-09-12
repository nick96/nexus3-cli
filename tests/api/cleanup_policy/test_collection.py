import json
import pytest

from nexuscli import exception
from nexuscli.api.cleanup_policy import CleanupPolicy


def test_get_by_name(nexus_mock_client, cleanup_policy_configuration):
    """
    It returns an instance of CleanupPolicy with the configuration given by the
    nexus script
    """
    response = {'result': json.dumps(cleanup_policy_configuration)}
    x_name = cleanup_policy_configuration['name']
    nexus_mock_client.cleanup_policies.run_script.return_value = response

    cleanup_policy = nexus_mock_client.cleanup_policies.get_by_name(x_name)

    assert cleanup_policy.configuration == cleanup_policy_configuration
    assert isinstance(cleanup_policy, CleanupPolicy)


def test_get_by_name_exception(nexus_mock_client, faker):
    """ It raises the documented exception when the policy name isn't found"""
    xname = faker.pystr()
    nexus_mock_client.cleanup_policies.run_script.side_effect = exception.NexusClientAPIError(
        xname)

    with pytest.raises(exception.NexusClientInvalidCleanupPolicy):
        nexus_mock_client.cleanup_policies.get_by_name(xname)


def test_create_or_update(nexus_mock_client, cleanup_policy_configuration, create_response):
    """"""
    cleanup_policy = CleanupPolicy(None, **cleanup_policy_configuration)
    response = create_response(cleanup_policy_configuration)
    nexus_mock_client.cleanup_policies.run_script.return_value = response

    nexus_mock_client.cleanup_policies.create_or_update(cleanup_policy)

    nexus_mock_client.cleanup_policies.run_script.assert_called_once()


@pytest.mark.integration
def test_maven(nexus_client, faker):
    policy_name = faker.pystr()
    repository_name = faker.pystr()
    configuration = {
        "name": policy_name,
        "format": "maven",  # the CLI passes maven, not maven2
        "mode": "delete",
        "criteria": {}
    }
    policy = CleanupPolicy(nexus_http=nexus_client.http, **configuration)
    nexus_client.cleanup_policies.create_or_update(policy)

    repository = nexus_client.repositories.new(
        'hosted', recipe='maven', name=repository_name, cleanup_policy=policy_name)
    nexus_client.repositories.create(repository)

    repository2 = nexus_client.repositories.get_by_name(repository_name)

    assert repository2.cleanup_policy == repository.cleanup_policy
