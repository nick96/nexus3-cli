from nexuscli.api.repository.recipes import validations
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['MavenGroupRepository', 'MavenHostedRepository', 'MavenProxyRepository']


class _MavenRepository(Repository):
    """
    A base `Maven
    <https://help.sonatype.com/repomanager3/formats/maven-repositories#MavenRepositories-MavenRepositoryFormat>`_
    Nexus repository.

    :param name: name of the repository.
    :type name: str
    :param layout_policy: one of :py:attr:`LAYOUT_POLICIES`. See Nexus
        documentation for details.
    :param version_policy: one of :py:attr:`VERSION_POLICIES`. See Nexus
        documentation for details.
    :param kwargs: see :class:`Repository`
    """
    DEFAULT_RECIPE = 'maven'
    RECIPES = ('maven',)
    LAYOUT_POLICIES = ('PERMISSIVE', 'STRICT')
    """Maven layout policies"""
    VERSION_POLICIES = ('RELEASE', 'SNAPSHOT', 'MIXED')
    """Maven version policies"""

    def __init__(self, name,
                 layout_policy='PERMISSIVE',
                 version_policy='RELEASE',
                 **kwargs):
        self.layout_policy = layout_policy
        self.version_policy = version_policy

        kwargs.update({'recipe': 'maven'})

        super().__init__(name, **kwargs)

        self.__validate_params()

    def __validate_params(self):
        validations.ensure_known(
            'layout_policy', self.layout_policy, self.LAYOUT_POLICIES)
        validations.ensure_known(
            'version_policy', self.version_policy, self.VERSION_POLICIES)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes']['maven'] = {
            'layoutPolicy': self.layout_policy,
            'versionPolicy': self.version_policy,
        }

        return repo_config

    @property
    def recipe_name(self):
        return 'maven2'


class MavenHostedRepository(HostedRepository, _MavenRepository):
    """
    A `Maven
    <https://help.sonatype.com/repomanager3/formats/maven-repositories#MavenRepositories-MavenRepositoryFormat>`_
    hosted Nexus repository.

    See :class:`HostedRepository` and :class:`MavenRepository`
    """
    pass


class MavenProxyRepository(_MavenRepository, ProxyRepository):
    """
    A `Maven
    <https://help.sonatype.com/repomanager3/formats/maven-repositories#MavenRepositories-MavenRepositoryFormat>`_
    proxy Nexus repository.

    See :class:`MavenRepository` and :class:`ProxyRepository`
    """
    pass


class MavenGroupRepository:
    def __init__(self):
        raise NotImplementedError
