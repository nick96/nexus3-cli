from nexuscli.api.repository.recipes.base import Repository
from nexuscli.api.repository.recipes.base_hosted import HostedRepository
from nexuscli.api.repository.recipes.base_proxy import ProxyRepository
from nexuscli.api.repository.recipes.base_group import GroupRepository

from nexuscli.api.repository.recipes.apt import *
from nexuscli.api.repository.recipes.bower import *
from nexuscli.api.repository.recipes.docker import *
from nexuscli.api.repository.recipes.maven import *
from nexuscli.api.repository.recipes.npm import *
from nexuscli.api.repository.recipes.nuget import *
from nexuscli.api.repository.recipes.pypi import *
from nexuscli.api.repository.recipes.raw import *
from nexuscli.api.repository.recipes.rubygems import *
from nexuscli.api.repository.recipes.yum import *

# FIXME: these are supposed to be strings
__all__ = [
    Repository, HostedRepository, ProxyRepository, GroupRepository,
    AptHostedRepository, AptProxyRepository,
    BowerGroupRepository, BowerHostedRepository, BowerProxyRepository,
    DockerHostedRepository, DockerProxyRepository,
    MavenHostedRepository, MavenProxyRepository,
    NpmGroupRepository, NpmHostedRepository, NpmProxyRepository,
    NugetGroupRepository, NugetHostedRepository, NugetProxyRepository,
    PypiGroupRepository, PypiHostedRepository, PypiProxyRepository,
    RawGroupRepository, RawHostedRepository, RawProxyRepository,
    RubygemsGroupRepository, RubygemsHostedRepository, RubygemsProxyRepository,
    YumHostedRepository, YumProxyRepository,
]

SUPPORTED_FORMATS = sorted(
    set([recipe for cls in __all__ for recipe in cls.RECIPES]))
