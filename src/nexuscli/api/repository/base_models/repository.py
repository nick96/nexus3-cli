from typing import Optional

import semver

from nexuscli.api.repository.base_models.base_repository import BaseRepository

# https://issues.sonatype.org/browse/NEXUS-19525
# https://github.com/thiagofigueiro/nexus3-cli/issues/77
CLEANUP_SET_MIN_VERSION = semver.VersionInfo(3, 19, 0)


class Repository(BaseRepository):
    """
    Representation of the simplest Nexus repositories.

    Nexus 3 repository recipes (formats) supported by this class:

        - `bower
          <https://help.sonatype.com/repomanager3/formats/bower-repositories>`_
        - `npm
          <https://help.sonatype.com/repomanager3/formats/npm-registry>`_
        - `nuget
          <https://help.sonatype.com/repomanager3/formats/nuget-repositories>`_
        - `pypi
          <https://help.sonatype.com/repomanager3/formats/pypi-repositories>`_
        - `raw
          <https://help.sonatype.com/repomanager3/formats/raw-repositories>`_
        - `rubygems
          <https://help.sonatype.com/repomanager3/formats/rubygems-repositories>`_
        - `docker
          <https://help.sonatype.com/repomanager3/formats/docker-registry>`_
        - `apt
          <https://help.sonatype.com/repomanager3/formats/apt-repositories>`_
    :param name: name of the repository.
    :param nexus_client: the :class:`~nexuscli.nexus_client.NexusClient`
        instance that will be used to perform operations against the Nexus 3
        service. You must provide this at instantiation or set it before
        calling any methods that require connectivity to Nexus.
    :param recipe: format (recipe) of the new repository. Must be one of
        :py:attr:`RECIPES`. See Nexus documentation for details.
    :param blob_store_name: name of an existing blob store; 'default'
        should work on most installations.
    :param strict_content_type_validation: Whether to validate file
        extension against its content type.
    :param cleanup_policy: name of an existing repository clean-up policy.
    """

    RECIPES = ('bower', 'npm', 'nuget', 'pypi', 'raw', 'rubygems')
    TYPE = None

    def __init__(self, name: str, cleanup_policy: Optional[str] = None, **kwargs):
        super().__init__(name, **kwargs)
        self._cleanup_policy = cleanup_policy

    def _cleanup_uses_set(self):
        # In case Sonatype changes the version string format, default to the
        # new behaviour as there should be more people using newer versions
        if self.nexus_client.server_version is None:
            return True

        # When the breaking API change was introduced
        if self.nexus_client.server_version >= CLEANUP_SET_MIN_VERSION:
            return True

        return False

    @property
    def cleanup_policy(self):
        """
        Groovy-formatted value for the cleanup/policy attribute.
        """
        if self._cleanup_uses_set():
            return [self._cleanup_policy]
        else:
            return self._cleanup_policy
