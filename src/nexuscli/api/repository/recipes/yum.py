from nexuscli import exception
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['YumGroupRepository', 'YumHostedRepository', 'YumProxyRepository']


class _YumRepository(Repository):
    """
    A `Yum <https://help.sonatype.com/repomanager3/formats/yum-repositories>`_
    base Nexus repository.

    :param name: name of the repository.
    :type name: str
    :param depth: The Yum ``repodata`` depth. Usually 1.
    :type depth: int
    :param kwargs: see :class:`Repository`
    """
    DEFAULT_RECIPE = 'yum'
    RECIPES = ('yum',)

    def __init__(self, name, depth=1, **kwargs):
        self.depth = depth

        kwargs.update({'recipe': 'yum'})

        super().__init__(name, **kwargs)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration
        repo_config['attributes']['yum'] = {
            'repodataDepth': self.depth
        }
        return repo_config


class YumHostedRepository(HostedRepository, _YumRepository):
    """
    A `Yum <https://help.sonatype.com/repomanager3/formats/yum-repositories>`_
    hosted Nexus repository.

    See :class:`HostedRepository` and :class:`YumRepository`
    """
    def upload_file(self, src_file, dst_dir, dst_file):
        """
        Upload a single file to a yum repository.

        :param self: repository instance used to access Nexus 3 service.
        :type self: nexuscli.api.repository.model.Repository
        :param src_file: path to the local file to be uploaded.
        :param dst_dir: directory under dst_repo to place file in.
        :param dst_file: destination file name.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        dst_dir = dst_dir or self.REMOTE_PATH_SEPARATOR
        repository_path = self.REMOTE_PATH_SEPARATOR.join(
            ['repository', self.name, dst_dir, dst_file])

        with open(src_file, 'rb') as fh:
            response = self.nexus_client.http_put(
                repository_path, data=fh, stream=True,
                service_url=self.nexus_client.config.url)

        if response.status_code != 200:
            raise exception.NexusClientAPIError(
                f'Uploading to {repository_path}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class YumProxyRepository(ProxyRepository, _YumRepository):
    """
    A `Yum <https://help.sonatype.com/repomanager3/formats/yum-repositories>`_
    proxy Nexus repository.

    See :class:`ProxyRepository` and :class:`YumRepository`
    """


class YumGroupRepository:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
