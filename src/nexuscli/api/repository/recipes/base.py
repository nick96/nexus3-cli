import semver

from nexuscli.api.repository.recipes import validations

DEFAULT_WRITE_POLICY = 'ALLOW'
DEFAULT_BLOB_STORE_NAME = 'default'
DEFAULT_STRICT_CONTENT = False

# https://issues.sonatype.org/browse/NEXUS-19525
# https://github.com/thiagofigueiro/nexus3-cli/issues/77
CLEANUP_SET_MIN_VERSION = semver.VersionInfo(3, 19, 0)


class BaseRepository:
    """
    The base class for Nexus repositories.

    :param name: name of the repository.
    :type name: str
    :param nexus_client: the :class:`~nexuscli.nexus_client.NexusClient`
        instance that will be used to perform operations against the Nexus 3
        service. You must provide this at instantiation or set it before
        calling any methods that require connectivity to Nexus.
    :type nexus_client: nexuscli.nexus_client.NexusClient
    :param recipe: format (recipe) of the new repository. Must be one of
        :py:attr:`RECIPES`. See Nexus documentation for details.
    :type recipe: str
    :param blob_store_name: name of an existing blob store; 'default'
        should work on most installations.
    :type blob_store_name: str
    :param strict_content_type_validation: Whether to validate file
        extension against its content type.
    :type strict_content_type_validation: bool
    """
    RECIPES = ()
    """The repository recipes supported by this class"""
    TYPE = None
    """The repository type supported by this class"""
    # TODO: refactor this so derived classes don't even accept a `recipe` kwarg
    DEFAULT_RECIPE = None
    """If a recipe is not given during initialisation, use this one as the default"""

    def __init__(self, name,
                 nexus_client=None,
                 recipe=None,
                 blob_store_name=DEFAULT_BLOB_STORE_NAME,
                 strict_content_type_validation=DEFAULT_STRICT_CONTENT,
                 ):
        self.name = name
        self.nexus_client = nexus_client
        # TODO: remove this the RECIPES attributes; no longer needed as there's
        #   a unique class for each recipe/type.
        self.recipe = (recipe or self.DEFAULT_RECIPE).lower()
        self.blob_store_name = blob_store_name
        self.strict_content = strict_content_type_validation

        self.__validate_params()

    def __repr__(self):
        return f'{self.__class__.__name__}-{self.name}'

    def __validate_params(self):
        validations.ensure_known('recipe', self.recipe, self.RECIPES)

    @property
    def recipe_name(self):
        """
        The Nexus 3 name for this repository's recipe (format). This is almost
        always the same as :attr:`name` with ``maven`` being the notable
        exception.
        """
        return self.recipe

    @property
    def configuration(self):
        """
        Repository configuration represented as a python dict. The dict
        returned by this property can be converted to JSON for use with the
        ``nexus3-cli-repository-create``
        groovy script created by the
        :py:meth:`~nexuscli.api.repository.collection.RepositoryCollection.create`
        method.

        Example structure and attributes common to all repositories:

        >>> common_configuration = {
        >>>     'name': 'my-repository',
        >>>     'online': True,
        >>>     'recipeName': 'raw',
        >>>     '_state': 'present',
        >>>     'attributes': {
        >>>         'storage': {
        >>>             'blobStoreName': 'default',
        >>>         },
        >>>         'cleanup': {
        >>>             'policyName': None,
        >>>         }
        >>>     }
        >>> }

        Depending on the repository type and format (recipe), other attributes
        will be present.

        :return: repository configuration
        :rtype: dict
        """
        repo_config = {
            'name': self.name,
            'online': True,
            'recipeName': f'{self.recipe_name}-{self.TYPE}',
            '_state': 'present',
            'attributes': {
                'storage': {
                    'blobStoreName': self.blob_store_name,
                    'strictContentTypeValidation': self.strict_content,
                },
            }
        }

        # we want 'x' or ['x'] but not None or [None]
        if self.cleanup_policy and any(self.cleanup_policy):
            repo_config['attributes']['cleanup'] = {
                'policyName': self.cleanup_policy}

        return repo_config


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
    :type name: str
    :param nexus_client: the :class:`~nexuscli.nexus_client.NexusClient`
        instance that will be used to perform operations against the Nexus 3
        service. You must provide this at instantiation or set it before
        calling any methods that require connectivity to Nexus.
    :type nexus_client: nexuscli.nexus_client.NexusClient
    :param recipe: format (recipe) of the new repository. Must be one of
        :py:attr:`RECIPES`. See Nexus documentation for details.
    :type recipe: str
    :param blob_store_name: name of an existing blob store; 'default'
        should work on most installations.
    :type blob_store_name: str
    :param strict_content_type_validation: Whether to validate file
        extension against its content type.
    :type strict_content_type_validation: bool
    :param cleanup_policy: name of an existing repository clean-up policy.
    :type cleanup_policy: str
    """

    RECIPES = (
        'bower',
        'npm',
        'nuget',
        'pypi',
        'raw',
        'rubygems',
    )
    TYPE = None

    def __init__(self, name, cleanup_policy=None, **kwargs):
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
