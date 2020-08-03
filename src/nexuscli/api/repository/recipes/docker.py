from nexuscli.api.repository.recipes import validations
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['DockerGroupRepository', 'DockerHostedRepository', 'DockerProxyRepository']


class _DockerRepository(Repository):
    DEFAULT_RECIPE = 'docker'
    RECIPES = ('docker',)

    def __init__(self, name,
                 http_port=8084,
                 https_port=8085,
                 v1_enabled=False,
                 force_basic_auth=False,
                 **kwargs):
        self.https_port = https_port
        self.http_port = http_port
        self.v1_enabled = v1_enabled
        self.force_basic_auth = force_basic_auth
        kwargs.update({'recipe': 'docker'})
        super().__init__(name, **kwargs)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes'].update({
            'docker': {
                'httpPort': self.http_port,
                'httpsPort': self.https_port,
                'v1Enabled': self.v1_enabled,
                'forceBasicAuth': self.force_basic_auth
            }
        })

        return repo_config


class DockerHostedRepository(HostedRepository, _DockerRepository):
    pass


class DockerProxyRepository(ProxyRepository, _DockerRepository):
    INDEX_TYPES = ('REGISTRY', 'HUB', 'CUSTOM')

    def __init__(self, name,
                 index_type='REGISTRY',
                 use_trust_store_for_index_access=False,
                 index_url='https://index.docker.io/',
                 **kwargs):
        self.index_type = index_type

        validations.ensure_known(
            'index_type',
            self.index_type,
            self.INDEX_TYPES
        )

        self.use_trust_store_for_index_access =\
            use_trust_store_for_index_access
        self.index_url = index_url
        super().__init__(name, **kwargs)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        if self.index_type == 'REGISTRY':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type
                },
            })
        if self.index_type == 'HUB':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type,
                    "useTrustStoreForIndexAccess":
                        self.use_trust_store_for_index_access

                },
            })
        if self.index_type == 'CUSTOM':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type,
                    "useTrustStoreForIndexAccess":
                        self.use_trust_store_for_index_access,
                    "indexUrl": self.index_url,
                },
            })
        return repo_config


class DockerGroupRepository:
    def __init__(self):
        raise NotImplementedError
