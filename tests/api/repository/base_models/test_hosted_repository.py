import itertools
import pytest

from nexuscli.api.repository import collection
from nexuscli.api.repository.base_models import HostedRepository


@pytest.mark.parametrize('repo_class, write_policy', itertools.product(
    [x for x in collection.get_classes_by_type('hosted')],
    HostedRepository.WRITE_POLICIES,
))
def test_configuration(repo_class, write_policy, nexus_mock_http, faker):
    """Ensure the property returns the attributes required/supported by Nexus"""

    kwargs = {
        'write_policy': write_policy,
    }

    repo = repo_class(name='dummy',  **kwargs)
    configuration = repo.configuration
    attributes = configuration['attributes']

    assert configuration['recipeName'] == repo._nexus_recipe_name
    assert attributes['storage']['writePolicy'] == write_policy
