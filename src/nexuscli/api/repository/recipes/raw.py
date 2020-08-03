import os

from nexuscli import exception
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['RawHostedRepository', 'RawProxyRepository', 'RawGroupRepository']


class _RawRepository:
    DEFAULT_RECIPE = 'raw'


class RawGroupRepository(_RawRepository, GroupRepository):
    pass


class RawHostedRepository(_RawRepository, HostedRepository):
    def upload_file(self, src_file, dst_dir, dst_file=None):
        """
        Upload a single file to a raw repository.

        :param src_file: path to the local file to be uploaded.
        :param dst_dir: directory under dst_repo to place file in. When None,
            the file is placed under the root of the raw repository
        :param dst_file: destination file name.
        :raises exception.NexusClientInvalidRepositoryPath: invalid repository
            path.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        dst_dir = os.path.normpath(dst_dir or self.REMOTE_PATH_SEPARATOR)
        if dst_file is None:
            dst_file = os.path.basename(src_file)

        params = {'repository': self.name}
        files = {'raw.asset1': open(src_file, 'rb').read()}
        data = {
            'raw.directory': dst_dir,
            'raw.asset1.filename': dst_file,
        }

        response = self.nexus_client.http_post(
            'components', files=files, data=data, params=params, stream=True)

        if response.status_code != 204:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class RawProxyRepository(_RawRepository, ProxyRepository):
    pass
