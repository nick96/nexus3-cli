Examples
--------

Here are some basic operations to get you started. Every command available on the CLI uses this API
interface, so the source code in ``src/nexuscli/nexus_client.py`` and ``src/nexuscli/cli/`` is a
good source of examples.

In all examples below you will need to instantiate a client:

.. code-block:: python

   import nexuscli, pprint
   nexus_config = nexuscli.nexus_config.NexusConfig()
   nexus_config.load()  # read config from ~/.nexus-cli
   nexus_client = nexuscli.nexus_client.NexusClient(config=nexus_config)


Get list of repositories
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   nexus_client.repositories.list
   [{'attributes': {},
   'format': 'maven2',
   'name': 'maven-snapshots',
   'type': 'hosted',
   'url': 'http://localhost:8081/repository/maven-snapshots'},
   {'attributes': {'proxy': {'remoteUrl': 'https://repo1.maven.org/maven2/'}},
   'format': 'maven2',
   'name': 'maven-central',
   'type': 'proxy',
   'url': 'http://localhost:8081/repository/maven-central'},
   {'attributes': {},
   'format': 'nuget',
   'name': 'nuget-group',
   'type': 'group',
   'url': 'http://localhost:8081/repository/nuget-group'},
   {'attributes': {'proxy': {'remoteUrl': 'https://www.nuget.org/api/v2/'}},
   'format': 'nuget',
   'name': 'nuget.org-proxy',
   'type': 'proxy',
   'url': 'http://localhost:8081/repository/nuget.org-proxy'},
   {'attributes': {},
   'format': 'maven2',
   'name': 'maven-releases',
   'type': 'hosted',
   'url': 'http://localhost:8081/repository/maven-releases'},
   {'attributes': {},
   'format': 'nuget',
   'name': 'nuget-hosted',
   'type': 'hosted',
   'url': 'http://localhost:8081/repository/nuget-hosted'},
   {'attributes': {},
   'format': 'maven2',
   'name': 'maven-public',
   'type': 'group',
   'url': 'http://localhost:8081/repository/maven-public'}]


Load a server repository into a local object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   r = nexus_client.repositories.get_by_name('maven-central')
   r.cleanup_policy
   [None]
   r.strict_content
   False
   r.version_policy
   'RELEASE'


Create a repository
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from nexuscli.api.repository.model import RawHostedRepository

   r = RawHostedRepository(
       name='my-repository',
       blob_store_name='default',
       strict_content_type_validation=False,
       write_policy='ALLOW',
   )

   nexus_client.repositories.create(r)

   nexus_client.repositories.get_raw_by_name('my-repository')
  {'name': 'my-repository',
   'format': 'raw',
   'type': 'hosted',
   'url': 'http://localhost:8081/repository/my-repository'}


Delete a repository
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   nexus_client.repositories.delete('my-repository')

   nexus_client.repositories.get_raw_by_name('my-repository')

   NexusClientInvalidRepository: my-repository

Upload a file
^^^^^^^^^^^^^

.. code-block:: python

   repository = nexus_client.repositories.get_by_name('my-repository')
   repository.upload('/etc/passwd', '/etc/passwd')
   1
   list(repository.list('/'))
   ['etc/passwd']


Upload a directory
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   repository.upload_directory('src/nexuscli/api', '/thats-a-lot-of-files')
   125
   len(list(repository.list('/')))
   125
   list(repository.list('/'))[:5]
   ['thats-a-lot-of-files/util.py',
    'thats-a-lot-of-files/__init__.py',
    'thats-a-lot-of-files/base_collection.py',
    'thats-a-lot-of-files/base_model.py',
    'thats-a-lot-of-files/repository/__init__.py']
