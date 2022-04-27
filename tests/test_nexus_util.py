import itertools
import os

import pytest

from nexuscli import exception, nexus_util
from nexuscli.nexus_util import calculate_hash


@pytest.mark.parametrize('hash_name, x_hash', [
    ('md5', '56c7e01b8db73367c174401f196a99ff'),
    ('sha1', 'e440325381d729a7f328bb6d3b8fdbe2fbe2ce74'),
    ('sha256',
     'dcdb8c8f2f95f40f311edd7c7d613a02a3cc5277d67a30e0d0a7bf88cae09b97'),
])
def test__calculate_hash(hash_name, x_hash, nexus_mock_client):
    """
    Ensure the method returns the correct hash for each algorithm using a known
    file with hash generated using another tool (MacOS shasum and md5 cli).
    """
    fixture = 'tests/fixtures/manifest-target/foo/bar.txt'

    sha1_file = calculate_hash(hash_name, fixture)
    with open(fixture, 'rb') as fh:
        sha1_fh = calculate_hash(hash_name, fh)

    assert sha1_fh == sha1_file
    assert sha1_fh == x_hash


@pytest.mark.parametrize('hash_name, match',
                         itertools.product(['sha1', 'md5'], [True, False]))
def test_has_same_hash(hash_name, match, mocker, faker):
    """Ensure method returns True when checksum matches and False otherwise"""
    file_path = faker.file_path()
    remote_hash = getattr(faker, hash_name)()
    if match:
        local_hash = remote_hash
    else:
        local_hash = getattr(faker, hash_name)()

    mocker.patch('nexuscli.nexus_util.calculate_hash', return_value=local_hash)
    artefact = {'checksum': {hash_name: remote_hash}}

    assert match == nexus_util.has_same_hash(artefact, file_path)
    nexus_util.calculate_hash.assert_called_with(hash_name, file_path)


def test_has_same_hash_empty():
    """Ensure method returns false when artefact has no checksum entries"""
    assert not nexus_util.has_same_hash({}, 'any')


@pytest.mark.parametrize('is_dir', [True, False])
def test_ensure_exists(is_dir, tmp_path, faker):
    """Ensure method calls the right combination of mkdir/touch"""
    path = tmp_path.joinpath(faker.word())

    nexus_util.ensure_exists(path, is_dir=is_dir)

    assert path.exists()
    assert is_dir == path.is_dir()
    assert is_dir != path.is_file()


@pytest.mark.parametrize(
    'component_path, x_repo, x_dir, x_file', [
        ('some/path/', 'some', 'path', None),
        ('some/other/path/', 'some', 'other/path', None),
        ('some/path/file', 'some', 'path', 'file'),
        ('some/other/path/file', 'some', 'other/path', 'file'),
        ('some/path/file.ext', 'some', 'path', 'file.ext'),
        ('repo', 'repo', None, None),
        ('repo/', 'repo', None, None),
        ('repo/.', 'repo', None, None),
        ('repo/./', 'repo', None, None),
        ('repo/./file', 'repo', None, 'file'),
        ('repo/file', 'repo', None, 'file'),
    ]
)
def test_split_component_path(component_path, x_repo, x_dir, x_file):
    repository, directory, filename = nexus_util.split_component_path(
        component_path)

    assert repository == x_repo
    assert directory == x_dir
    assert filename == x_file


@pytest.mark.parametrize(
    'component_path, x_error', [
        ('', 'does not contain a repository'),
        ('.', 'does not contain a repository'),
        ('./', 'does not contain a repository'),
    ]
)
def test_split_component_path_errors(component_path, x_error):
    with pytest.raises(exception.NexusClientInvalidRepositoryPath) as e:
        nexus_util.split_component_path(component_path)

    assert x_error in str(e.value)


@pytest.mark.parametrize('flatten, remote, destination, x_local_path', [
    # no rename (file to dir)
    (False, 'file', '.',            '_TMP_file'),
    (False, 'file', './',           '_TMP_file'),
    (False, 'file', '..',           '_TMP_../file'),
    (False, 'file', '../',          '_TMP_../file'),
    (False, 'file', '/',            '/file'),
    (False, 'file', '/dir/',        '/dir/file'),
    (False, 'file', 'dir/',         '_TMP_dir/file'),
    (False, 'file', 'dir/sub/',     '_TMP_dir/sub/file'),
    (False, 'file', '/dir/sub/',    '/dir/sub/file'),

    # rename (file to file)
    (False, 'file', 'file2',        '_TMP_file2'),
    (False, 'file', './file2',      '_TMP_file2'),
    (False, 'file', '/file2',       '/file2'),
    (False, 'file', '/dir/file2',   '/dir/file2'),
    (False, 'file', 'dir/file2',    '_TMP_dir/file2'),

    # remote has directory, no rename
    (False, 'dir/file', '.',         '_TMP_dir/file'),
    (True,  'dir/file', '.',         '_TMP_file'),
    (False, 'dir/file', './',        '_TMP_dir/file'),
    (True,  'dir/file', './',        '_TMP_file'),
    (False, 'dir/file', '..',        '_TMP_../dir/file'),
    (True,  'dir/file', '..',        '_TMP_../file'),
    (False, 'dir/file', '../',       '_TMP_../dir/file'),
    (True,  'dir/file', '../',       '_TMP_../file'),
    (False, 'dir/file', '/',         '/dir/file'),
    (True,  'dir/file', '/',         '/file'),
    (False, 'dir/file', '/dir/',     '/dir/dir/file'),
    (True,  'dir/file', '/dir/',     '/dir/file'),
    (False, 'dir/file', 'dir/',      '_TMP_dir/dir/file'),
    (True,  'dir/file', 'dir/',      '_TMP_dir/file'),
    (False, 'dir/file', 'dir/sub/',  '_TMP_dir/sub/dir/file'),
    (True,  'dir/file', 'dir/sub/',  '_TMP_dir/sub/file'),
    (False, 'dir/file', '/dir/sub/', '/dir/sub/dir/file'),
    (True,  'dir/file', '/dir/sub/', '/dir/sub/file'),

    # remote has directory, rename
    (False, 'dir1/file', 'file2',      '_TMP_dir1/file2'),
    (True,  'dir1/file', 'file2',       '_TMP_file2'),
    (False, 'dir1/file', './file2',     '_TMP_dir1/file2'),
    (True,  'dir1/file', './file2',     '_TMP_file2'),
    (False, 'dir1/file', '/file2',      '/dir1/file2'),
    (True,  'dir1/file', '/file2',      '/file2'),
    (False, 'dir1/file', '/dir2/file2', '/dir2/dir1/file2'),
    (True,  'dir1/file', '/dir2/file2', '/dir2/file2'),
    (False, 'dir1/file', 'dir2/file2',  '_TMP_dir2/dir1/file2'),
    (True,  'dir1/file', 'dir2/file2',  '_TMP_dir2/file2'),
])
def test_remote_path_to_local(flatten, remote, destination, x_local_path, tmpdir):
    """
    Ensure the method correctly resolves a remote path to a local destination,
    following the instance setting for flatten.
    """
    # add cwd to expected result as the fixture gives it as relative but the
    # method always returns an absolute path
    if x_local_path.find('_TMP_') == 0:
        x_local_path = x_local_path.replace('_TMP_', str(tmpdir) + os.sep)

    with tmpdir.as_cwd():
        local_path = nexus_util.remote_path_to_local(remote, destination, flatten, create=False)

    assert str(local_path) == x_local_path


@pytest.mark.parametrize('is_dst_dir, flatten', ([False, True], [False, True]))
def test_remote_path_to_local_create(faker, flatten, is_dst_dir, tmpdir):
    """Ensure the method creates a file or directory, according to given parameters"""
    # use a relative path as destination; another test covers abs/rel paths
    local_dst = faker.file_path(depth=faker.random_int(2, 10))[1:]
    assert_type = os.path.isfile
    if is_dst_dir:
        assert_type = os.path.isdir
        local_dst += os.sep

    with tmpdir.as_cwd():
        local_path = nexus_util.remote_path_to_local('a', local_dst, flatten=flatten, create=True)
        assert assert_type(local_dst)
        assert os.path.isfile(local_path)
