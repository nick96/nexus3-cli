import pytest

from nexuscli import exception


@pytest.mark.integration
def test_activate(nexus_client, faker):
    """Ensure method raises expected exception when it can't activate a realm"""
    missing_realm = faker.pystr()
    with pytest.raises(exception.NexusClientAPIError):
        nexus_client.security_realms.activate(missing_realm)
