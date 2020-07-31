from nexuscli.api.repository.recipes.base_hosted import HostedRepository
from nexuscli.api.repository.recipes.base_group import GroupRepository
from nexuscli.api.repository.recipes.base_proxy import ProxyRepository

__all__ = ['RubygemsHostedRepository', 'RubygemsProxyRepository', 'RubygemsGroupRepository']


class _RubygemsRepository:
    DEFAULT_RECIPE = 'rubygems'


class RubygemsGroupRepository(_RubygemsRepository, GroupRepository):
    pass


class RubygemsHostedRepository(_RubygemsRepository, HostedRepository):
    pass


class RubygemsProxyRepository(_RubygemsRepository, ProxyRepository):
    pass
