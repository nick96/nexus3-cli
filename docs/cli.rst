Command-line Interface
======================

Logging level can be configured by setting an environment variable named
``LOG_LEVEL``. Valid values are: ``DEBUG``, ``INFO``, ``WARNING`` (default),
``ERROR``, ``CRITICAL``.

The Nexus server and authentication options can also be set via environment variables:

    - `NEXUS3_PASSWORD` (required)
    - `NEXUS3_USERNAME` (required)
    - `NEXUS3_URL` (required)
    - `NEXUS3_API_VERSION` (optional)
    - `NEXUS3_X509_VERIFY` (optional)


.. click:: nexuscli.cli:nexus_cli
   :prog: nexus3
   :show-nested:
