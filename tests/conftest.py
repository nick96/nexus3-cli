import os
import pathlib
import pytest
import semver
import shutil
import tempfile
import time
from faker import Faker
from subprocess import check_call

from nexuscli.nexus_client import NexusClient
from nexuscli.nexus_config import NexusConfig
from nexuscli.nexus_http import NexusHttp


APT_GPG_KEY_PATH = pathlib.Path('tests/fixtures/apt/private.gpg.key')


@pytest.fixture
def apt_gpg_key_path():
    return APT_GPG_KEY_PATH


@pytest.fixture
def gpg_key_as_cwd(apt_gpg_key_path, tmp_path: pathlib.Path):
    shutil.copy(apt_gpg_key_path, tmp_path)
    old_path = pathlib.Path.cwd()
    os.chdir(tmp_path)

    try:
        yield
    finally:
        os.chdir(old_path)


@pytest.fixture
def docopt_args(faker):
    args = {
        '--blob': 'default',
        '--deploy': 'disable',
        '--depth': '0',
        '--help': False,
        '--help,': False,
        '--layout': 'strict',
        '--strict-content': False,
        '--version': 'release',
        '<repo_name>': faker.word(),
        '<script.groovy>': None,
        '<script_name>': None,
        'create': False,
        'hosted': False,
        'list': False,
        'login': False,
        'maven2': True,
        'npm': False,
        'pypi': False,
        'raw': False,
        'repository': False,
        'delete': False,
        'rubygems': False,
        'run': False,
        'script': False,
        'yum': False
    }

    return args


@pytest.fixture(scope='session')
def nexus_config():
    config = NexusConfig()
    config.load()
    return config


@pytest.fixture(scope='session')
def nexus_client(nexus_config):
    client = NexusClient(config=nexus_config)
    return client


def nexus_artefact():
    """
    See nexus_raw_response for raw_response format.
    """
    fake = Faker()

    fixture = {
        'checksum': {
            'md5': fake.md5(),
            'sha1': fake.sha1(),
            'sha256': fake.sha256(),
        },
        'downloadUrl': None,
        'format': None,
        'id': fake.pystr(min_chars=63, max_chars=63),
        'path': None,
        'repository': None,
    }

    return fixture


@pytest.helpers.register
def nexus_raw_response(file_list, repository=None):
    """
    Raw response looks like :
    >>> r = [{
    >>>         'checksum': {
    >>>             'md5': 'd94b865aa7620c46ef8faef7059a311c',
    >>>             'sha1': '2186934d880cf24dd9ecc578335e290026695522',
    >>>             'sha256': 'b7bb3424a6a6(...)4113bc38fd7807528481a8ffe3cf',
    >>>             'sha512': 'e7806f3caa3e(...)3caeb9bbc54bbde286c07f837fdc'
    >>>         },
    >>>         'downloadUrl': 'http://nexus/repository/repo_name/a/file.ext',
    >>>         'format': 'yum',
    >>>         'id': 'Y2xvdWRlcmEtbWFuYWdlcj(...)mRiNWU0YjllZWQzMg',
    >>>         'path': 'a/fake.rpm',
    >>>         'repository': 'cloudera-manager'
    >>> }]
    """
    for artefact_path in file_list:
        artefact = nexus_artefact()
        artefact['path'] = artefact_path
        artefact['repository'] = repository or 'some_repository'
        yield artefact


@pytest.fixture
def file_upload_args(faker):
    """A tuple of arguments suitable for use with NexusClient"""
    x_src_file = faker.file_path()[1:]  # relative paths make testing easier
    x_dst_file = os.path.basename(x_src_file)
    x_repo_name = faker.uri_page()
    x_dst_dir = faker.uri_path()

    return x_src_file, x_repo_name, x_dst_dir, x_dst_file


@pytest.helpers.register
def nexus_repository(name, format_):
    return {
        'name': name,
        'format': format_,
    }


@pytest.fixture
def nexus_mock_http(mocker, faker, config_args):
    class ResponseMock:
        def __init__(self):
            self.status_code = 200
            self.text = faker.sentence()
            self.content = faker.sentence()
            self.reason = faker.sentence()

            # prepare content for repositories.raw_list
            self._json = [
                nexus_repository(
                    name=faker.pystr(),
                    format_=faker.random.choice(
                        ['pypi', 'nuget', 'raw', 'yum', 'rubygems'])
                )
                for _ in range(faker.random_int(1, 10))
            ]

        def json(self):
            return self._json

    mocker.patch('nexuscli.nexus_http.NexusHttp.request', return_value=ResponseMock())
    mocker.patch('nexuscli.nexus_http.NexusHttp.server_version',
                 new_callable=mocker.PropertyMock, return_value=semver.VersionInfo(3, 19, 0))
    return NexusHttp(NexusConfig(**config_args))


@pytest.fixture
def nexus_mock_client(nexus_mock_http, mocker, faker):
    """A nexus_client with the request method mocked"""
    mocker.patch('nexuscli.api.base_collection.BaseCollection.run_script')
    mocker.patch.object(NexusClient, 'security_realms', new_callabe=mocker.PropertyMock)

    client = NexusClient()
    return client


def _deep_file_tree(faker, tmp_path):
    fixture = []
    with tmp_path:
        for _ in range(faker.random_int(1, 100)):
            relative_path = faker.file_path(
                depth=faker.random_number(1, 10))[1:]
            fixture.append(relative_path)
            tmp_path.joinpath(relative_path).parent.mkdir(
                parents=True, exist_ok=True)
            tmp_path.joinpath(relative_path).touch(exist_ok=True)

    return str(tmp_path), set(fixture)


@pytest.fixture
def deep_file_tree(faker, tmp_path):
    """
    Yields a tuple(str, set). The str is the current working directory. The
    list contains deep file paths, relative to the current working dir, where
    all files exist in the filesystem.
    """
    return _deep_file_tree(faker, tmp_path)


@pytest.fixture
def make_testfile(faker, tmpdir):
    """
    Yields a tuple(str, str). The 1st str is the current working directory.
    The 2ns string contains a file path, relative to the current working dir,
    where the files exist in the filesystem at the given depth.
    """
    with tmpdir.as_cwd():
        filename = faker.file_name()
        tmpdir.join(filename).ensure()

    yield str(tmpdir), filename


@pytest.helpers.register
def repo_list(repository, expected_count, repo_path=''):
    """
    Nexus doesn't show uploaded files when you list the contents immediately
    after an upload. This helper retries it 3 times with increasing back-off.
    """
    def _list():
        print(f'Listing files on {repository.name}/{repo_path}')
        file_list = repository.list(repo_path)

        files = []
        for f in iter(file_list):
            f = f[len(repo_path):] if repo_path else f
            files.append(f)

        return files

    attempt = 1
    file_set = set(_list())
    while len(file_set) != expected_count and attempt < 4:
        attempt += 1
        time.sleep(2 * attempt)
        file_set = set(_list())

    # let it fail if we run out of attempts
    return file_set


def _hosted_raw_repo_empty(faker):
    repo_name = faker.pystr()
    command = 'nexus3 repository create hosted raw {}'.format(repo_name)
    check_call(command.split())
    return repo_name


@pytest.fixture
def hosted_raw_repo_empty(faker):
    """Create an empty hosted raw repository"""
    return _hosted_raw_repo_empty(faker)


@pytest.fixture(scope='session')
def upload_repo():
    """As per hosted_raw_repo_empty but scoped for the session"""
    faker = Faker()
    tmp_path = pathlib.Path(tempfile.TemporaryDirectory().name)
    src_dir, x_file_list = _deep_file_tree(faker, tmp_path)
    return _hosted_raw_repo_empty(faker), src_dir, x_file_list


@pytest.fixture()
def response_mock():
    """Generate mock return value for request"""
    class ResponseMock:
        def __init__(self, status_code, reason):
            self.status_code = status_code
            self.reason = reason

    return ResponseMock


@pytest.fixture
def client_args(config_args):
    """Parameters suitable for use with NexusClient()"""
    fixture = {
        'config': config_args,
    }
    return fixture


@pytest.fixture
def config_args(faker, tmpdir):
    """Parameters suitable for use with NexusConfig()"""
    fixture = {
        'api_version': faker.pystr(),
        'username': faker.user_name(),
        'password': faker.password(),
        'url': faker.url(),
        'x509_verify': faker.pybool(),
        'config_path': str(tmpdir.join(faker.file_name())),
    }
    return fixture
