from nexuscli.api import validations
from nexuscli.api.base_model import BaseModel


class Blobstore(BaseModel):
    ALLOWED_TYPES = ['s3', 'file']  # validation uses lower-case

    def _validate_params(self) -> None:
        if not isinstance(self._raw.get('type'), str):
            raise ValueError('type must be a str')
        validations.ensure_known('type', self._raw['type'].lower(), self.ALLOWED_TYPES)
        self._raw['type'] = self._raw['type'].title()

        if not isinstance(self._raw.get('path'), str) or not self._raw.get('path'):
            raise ValueError('path must be a non-empty str')
        super()._validate_params()

        if self._raw.get('softQuota') is None:
            self._raw['softQuota'] = None

    @property
    def type(self) -> str:
        return self._raw['type'].lower()
