Groovy Scripts
==============

This package makes use of Groovy scripts to perform actions that are not
available through the Nexus 3 REST API.

All scripts added have names starting with ``nexus3-cli-``.

.. code-block:: console
   :emphasize-lines: 1

   $ nexus3 script list
   Name                                  Type     Content
   ------------------------------------------------------------------------------------------
   nexus3-cli-cleanup-policy_3.27.0      groovy   // Original from:
                                                  // https://github.com/...
   ------------------------------------------------------------------------------------------
   nexus3-cli-repository-delete          groovy   log.info("Deleting <repository=${args}>"...
   ------------------------------------------------------------------------------------------
   nexus3-cli-repository-get             groovy   import groovy.json.JsonBuilder

                                                  Boolean ...
   ------------------------------------------------------------------------------------------
   nexus3-cli-repository-create_3.21.0   groovy   import groovy.json.JsonSlurper
                                                  import or...

You can delete them all by running:

.. code-block:: console
   :emphasize-lines: 1

    $ nexus3 script list | grep ^nexus3- | awk '{ print $1 }' | xargs --no-run-if-empty -n1 nexus3 script del
    Name (type)

.. note::

   On macOS, remove the ``--no-run-if-empty`` as it's not supported by the BSD xargs.

To increase verbosity of logging for the scripts, create a new `logger
<https://help.sonatype.com/repomanager3/system-configuration/support-features#SupportFeatures-LoggingandLogViewer>`_
(e.g.: http://localhost:8081/#admin/support/logging) with logger name
``org.sonatype.nexus.script.plugin.internal.rest.ScriptResource`` and logging
level ``DEBUG`` or ``TRACE``.
