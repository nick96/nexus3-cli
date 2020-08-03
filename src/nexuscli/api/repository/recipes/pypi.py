from nexuscli import exception
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['PypiHostedRepository', 'PypiProxyRepository', 'PypiGroupRepository']


class _PypiRepository(Repository):
    DEFAULT_RECIPE = 'pypi'


class PypiGroupRepository(_PypiRepository, GroupRepository):
    pass


class PypiHostedRepository(_PypiRepository, HostedRepository):
    def upload_file(self, src_file, dst_dir=None, dst_file=None):
        """
        Upload a single file to a PyPI repository.

        :param src_file: path to the local file to be uploaded.
        :param dst_dir: NOT USED
        :param dst_file: NOT USED
        :raises exception.NexusClientInvalidRepositoryPath: invalid repository
            path.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        params = {'repository': self.name}
        files = {'pypi.asset': open(src_file, 'rb').read()}

        response = self.nexus_client.http_post(
            'components', files=files, params=params, stream=True)

        if response.status_code != 204:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class PypiProxyRepository(_PypiRepository, ProxyRepository):
    pass
