from nexuscli.api import util
from nexuscli.api.base_model import BaseModel


class Realm(BaseModel):
    """A Nexus 3 server security realm object."""
    @util.with_min_version('3.19.0')
    def activate(self) -> None:
        """Activate this security realm."""
        self._client.security_realms.activate(self.configuration['id'])
