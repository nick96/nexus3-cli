import pytest

from nexuscli.api.security.realms.model import Realm


@pytest.mark.integration
def test_activate(nexus_client, faker):
    """Ensure the method activates the given realm"""
    inactive_realms = [x.configuration['id']
                       for x in nexus_client.security_realms.collection
                       if not x.configuration['active']]
    x_activated_id = faker.random_element(inactive_realms)

    docker_realm = Realm(nexus_client, id=x_activated_id)

    docker_realm.activate()

    assert x_activated_id in nexus_client.security_realms.active
