##########
Change Log
##########

1.2.0 [2016-10-15]
==================

- Update shims to work with `validate_base <https://github.com/lsst/validate_base>`_ -type Job JSON (as of `DM-7042 <https://jira.lsstcorp.org/browse/DM-7042>`_). The JSON created for SQUASH is unchanged.
- There is now a `schema <http://json-schema.org>`_ for the JSON submitted to SQUASH. See ``postqa/schemas/squash.json`` and the ``postqa.schemas`` module. Tests use this schema with the ``jsonschema`` package to validate output JSON.
- Improved tests and coverage.

`DM-7041 <https://jira.lsstcorp.org/browse/DM-7041>`_.

1.1.1 [2016-10-14]
==================

- GitHub repo URLs of packages are now obtained from ``lsstsw/etc/repos.yaml`` itself. Previously post-qa could not accurately describe packages not in the github.com/lsst GitHub organization.

`DM-6374 <https://jira.lsstcorp.org/browse/DM-6374>`_.

1.1.0 [2016-08-12]
==================

- Add additional Jenkins environment variables to support multiple datasets.

`DM-7098 <https://jira.lsstcorp.org/browse/DM-7098>`_.

1.0.0 [2016-07-01]
==================

- Initial release

`DM-6308 <https://jira.lsstcorp.org/browse/DM-6308>`_.
