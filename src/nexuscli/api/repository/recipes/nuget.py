from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['NugetHostedRepository', 'NugetProxyRepository', 'NugetGroupRepository']


class _NugetRepository:
    DEFAULT_RECIPE = 'nuget'


class NugetGroupRepository(_NugetRepository, GroupRepository):
    pass


class NugetHostedRepository(_NugetRepository, HostedRepository):
    pass


class NugetProxyRepository(_NugetRepository, ProxyRepository):
    pass
