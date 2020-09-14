import pytest

from nexuscli.api.blobstore import Blobstore


@pytest.mark.parametrize('x_type', Blobstore.TYPES)
def test_type(x_type):
    """Ensure only allowed values for type are accepted"""
    b = Blobstore(type=x_type, name='dummy', path='dummy')
    assert b.type == x_type


@pytest.mark.parametrize('x_type', ['unknown', '', None])
def test__validate_params_type(x_type,):
    """Ensure invalid values for type raise an exception"""
    with pytest.raises(ValueError):
        Blobstore(type=x_type, name='dummy', path='dummy')


@pytest.mark.parametrize('path', ['', None])
def test__validate_params_path(path):
    """Ensure invalid values for path raise an exception"""
    with pytest.raises(ValueError):
        Blobstore(type='File', name='dummy', path=path)
