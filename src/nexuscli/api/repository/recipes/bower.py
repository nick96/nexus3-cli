from nexuscli.api.repository.recipes.base_hosted import HostedRepository
from nexuscli.api.repository.recipes.base_group import GroupRepository
from nexuscli.api.repository.recipes.base_proxy import ProxyRepository

__all__ = ['BowerHostedRepository', 'BowerProxyRepository', 'BowerGroupRepository']


class _BowerRepository:
    DEFAULT_RECIPE = 'bower'


class BowerGroupRepository(_BowerRepository, GroupRepository):
    pass


class BowerHostedRepository(_BowerRepository, HostedRepository):
    pass


class BowerProxyRepository(_BowerRepository, ProxyRepository):
    pass
