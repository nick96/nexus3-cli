import os

from clint.textui import progress

from nexuscli.api.repository.recipes import validations
from nexuscli.api.repository.base_models import util, Repository

DEFAULT_WRITE_POLICY = 'ALLOW'


class HostedRepository(Repository):
    """
    A hosted Nexus repository.

    :param name: name of the repository.
    :type name: str
    :param write_policy: one of :py:attr:`WRITE_POLICIES`. See Nexus
        documentation for details.
    :type write_policy: str
    :param kwargs: see :class:`Repository`
    """
    WRITE_POLICIES = ['ALLOW', 'ALLOW_ONCE', 'DENY']
    """Nexus 3 repository write policies supported by this class."""

    TYPE = 'hosted'

    def __init__(self, name, write_policy=DEFAULT_WRITE_POLICY, **kwargs):
        self.write_policy = write_policy

        super().__init__(name, **kwargs)

        self.__validate_params()

    def __validate_params(self):
        validations.ensure_known(
            'write_policy', self.write_policy, self.WRITE_POLICIES)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes']['storage'].update({
            'writePolicy': self.write_policy,
            'strictContentTypeValidation': self.strict_content,
        })

        return repo_config

    def upload_file(self, src_file, dst_dir, dst_file=None):
        raise NotImplementedError

    @classmethod
    def get_upload_subdirectory(cls, dst_dir, file_path, flatten=False):
        """
        Find the destination subdirectory based on given parameters. This is mostly
        so the `flatten` option is honoured.

        :param dst_dir: destination directory
        :param file_path: file path, using REMOTE_PATH_SEPARATOR as the directory
            separator.
        :param flatten: when True, sub_directory will be flattened (ie: file_path
            structure will not be present in the destination directory)
        :type flatten: bool
        :return: the appropriate sub directory in the destination directory.
        :rtype: str
        """
        # empty dst_dir because most repo formats, aside from raw, allow it
        sub_directory = dst_dir or ''
        if flatten:
            return sub_directory

        sep = cls.REMOTE_PATH_SEPARATOR
        dirname = os.path.dirname(file_path)
        if sub_directory.endswith(sep) or dirname.startswith(sep):
            sep = ''
        sub_directory += f'{sep}{dirname}'

        return sub_directory

    def upload_directory(self, src_dir, dst_dir, recurse=True, flatten=False):
        """
        Uploads all files in a directory to the specified destination directory
        in this repository, honouring options flatten and recurse.

        :param src_dir: path to local directory to be uploaded
        :param dst_dir: destination directory in dst_repo
        :param recurse: when True, upload directory recursively.
        :type recurse: bool
        :param flatten: when True, the source directory tree isn't replicated
            on the destination.
        :return: number of files uploaded
        :rtype: int
        """
        file_set = util.get_files(src_dir, recurse)
        file_count = len(file_set)
        file_set = progress.bar(file_set, expected_size=file_count)

        for relative_filepath in file_set:
            file_path = os.path.join(src_dir, relative_filepath)
            sub_directory = self.get_upload_subdirectory(
                dst_dir, file_path, flatten)
            self.upload_file(file_path, sub_directory)

        return file_count
