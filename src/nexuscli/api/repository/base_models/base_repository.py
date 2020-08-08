from typing import Optional

import nexuscli  # noqa: F401; for mypy
from nexuscli.api.repository.recipes import validations

DEFAULT_BLOB_STORE_NAME = 'default'
DEFAULT_STRICT_CONTENT = False


# TODO: inherit nexuscli.api.base_model.BaseModel`
class BaseRepository:
    """
    The base class for Nexus repositories.

    :param name: name of the repository.
    :param nexus_client: the :class:`~nexuscli.nexus_client.NexusClient`
        instance that will be used to perform operations against the Nexus 3
        service. You must provide this at instantiation or set it before
        calling any methods that require connectivity to Nexus.
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
    REMOTE_PATH_SEPARATOR = '/'
    """The character used by the Nexus server as a path separator"""
    RECIPES = ()
    """The repository recipes supported by this class"""
    TYPE = None
    """The repository type supported by this class"""
    # TODO: refactor this so derived classes don't even accept a `recipe` kwarg
    DEFAULT_RECIPE = None
    """If a recipe is not given during initialisation, use this one as the default"""

    def __init__(self, name: str,
                 nexus_client: Optional['nexuscli.nexus_client.NexusClient'] = None,
                 recipe: Optional[str] = None,
                 blob_store_name: str = DEFAULT_BLOB_STORE_NAME,
                 strict_content_type_validation: bool = DEFAULT_STRICT_CONTENT):
        self.name = name
        self.nexus_client = nexus_client
        # TODO: remove this the RECIPES attributes; no longer needed as there's
        #   a unique class for each recipe/type.
        self.recipe: Optional[str] = (recipe or self.DEFAULT_RECIPE)
        if self.recipe:
            self.recipe = self.recipe.lower()

        self.blob_store_name = blob_store_name
        self.strict_content = strict_content_type_validation

        self.__validate_params()

    def __repr__(self):
        return f'{self.__class__.__name__}-{self.name}'

    def __validate_params(self) -> None:
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
