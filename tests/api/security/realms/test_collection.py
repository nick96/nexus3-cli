import pytest

from nexuscli import exception


@pytest.mark.integration
def test_activate_error(nexus_client, faker):
    """Ensure method raises expected exception when it can't activate a realm"""
    missing_realm = faker.pystr()
    with pytest.raises(exception.NexusClientAPIError):
        nexus_client.security_realms.activate(missing_realm)


@pytest.mark.integration
def test_activate(nexus_client, faker):
    """Ensure the method activates the given realm"""
    inactive_realms = [x.configuration['id']
                       for x in nexus_client.security_realms.collection
                       if not x.configuration['active']]
    x_activated_id = faker.random_element(inactive_realms)

    nexus_client.security_realms.activate(x_activated_id)

    assert x_activated_id in nexus_client.security_realms.active
