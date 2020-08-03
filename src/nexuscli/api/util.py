import functools
import pathlib
import warnings
from typing import Any, Callable, TypeVar, cast

import semver

import nexuscli
from nexuscli import exception

# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar('F', bound=Callable[..., Any])


def script_for_version(script_name, server_version, versions):
    """
    Determine if a certain nexus server version requires a different version of
    the given groovy script.

    :param script_name: original name of the script.
    :param server_version: VersionInfo for the Nexus server.
    :param versions: list of VersionInfo. Each element represents an existing
        groovy script that must be used with server_version or greater.
    :return: the version-specific name of script_name.
    """
    if server_version is None:
        return script_name

    for breaking_version in sorted(versions, reverse=True):
        if server_version >= breaking_version:
            script_path = pathlib.Path(script_name)
            # e.g.: nexus3-cli-repository-create_3.21.0.groovy
            return f'{script_path.stem}_{breaking_version}{script_path.suffix}'

    return script_name


def with_min_version(min_version: str) -> Callable[[F], F]:
    """Verifies that the `nexus_client` instance has version greater or equal to min_version"""
    def decorator(f):
        @functools.wraps(f)
        # be explicit that args[0] is `self` in the context of the calling class instance
        def wrapper(collection: 'nexuscli.api.base_collection.BaseCollection', *args, **kwargs):
            try:
                min_semver = semver.VersionInfo.parse(min_version)
            except ValueError:
                warnings.warn(
                    'Invalid semver string; skipping version capability check', stacklevel=2)
                return f(collection, *args, **kwargs)

            if collection._client.server_version < min_semver:
                raise exception.NexusClientCapabilityUnsupported(
                    f'{f} requires version {min_semver}; server has '
                    f'version {collection._client.server_version}')

            return f(collection, *args, **kwargs)

        return cast(F, wrapper)
    return decorator
