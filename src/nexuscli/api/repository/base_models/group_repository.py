from nexuscli.api.repository.base_models.repository import Repository


class GroupRepository(Repository):
    """
    A group Nexus repository.

    :param name: name of the repository.
    :type name: str
    :param member_names: ordered name of repositories in the group
    :type member_names: list
    :param kwargs: see :class:`Repository`
    """
    RECIPES = Repository.RECIPES
    TYPE = 'group'

    def __init__(self, name, member_names=None, **kwargs):
        super().__init__(name, **kwargs)
        self.member_names = member_names or []

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration
        repo_config['attributes']['group'] = {
            'memberNames': self.member_names,
        }

        return repo_config
