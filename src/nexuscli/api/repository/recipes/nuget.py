from nexuscli.api.repository.recipes.base_hosted import HostedRepository
from nexuscli.api.repository.recipes.base_group import GroupRepository
from nexuscli.api.repository.recipes.base_proxy import ProxyRepository

__all__ = ['NugetHostedRepository', 'NugetProxyRepository', 'NugetGroupRepository']


class _NugetRepository:
    DEFAULT_RECIPE = 'nuget'


class NugetGroupRepository(_NugetRepository, GroupRepository):
    pass


class NugetHostedRepository(_NugetRepository, HostedRepository):
    pass


class NugetProxyRepository(_NugetRepository, ProxyRepository):
    pass
