jsontableschema-bigquery-py
===========================

| |Travis|
| |Coveralls|
| |PyPi|
| |SemVer|
| |Gitter|

Generate and load BigQuery tables based on JSON Table Schema
descriptors.

    Version ``v0.3`` contains breaking changes:

-  renamed ``Storage.tables`` to ``Storage.buckets``
-  changed ``Storage.read`` to read into memory
-  added ``Storage.iter`` to yield row by row

Getting Started
---------------

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install jsontableschema-bigquery

Storage
~~~~~~~

Package implements `Tabular
Storage <https://github.com/frictionlessdata/jsontableschema-py#storage>`__
interface.

To start using Google BigQuery service:

-  Create a new project -
   `link <https://console.developers.google.com/home/dashboard>`__
-  Create a service key -
   `link <https://console.developers.google.com/apis/credentials>`__
-  Download json credentials and set ``GOOGLE_APPLICATION_CREDENTIALS``
   environment variable

We can get storage this way:

.. code:: python

    import io
    import os
    import json
    from apiclient.discovery import build
    from oauth2client.client import GoogleCredentials
    from jsontableschema_bigquery import Storage

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
    credentials = GoogleCredentials.get_application_default()
    service = build('bigquery', 'v2', credentials=credentials)
    project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
    storage = Storage(service, project, 'dataset', prefix='prefix')

Then we could interact with storage:

.. code:: python

    storage.buckets
    storage.create('bucket', descriptor)
    storage.delete('bucket')
    storage.describe('bucket') # return descriptor
    storage.iter('bucket') # yields rows
    storage.read('bucket') # return rows
    storage.write('bucket', rows)

Mappings
~~~~~~~~

::

    schema.json -> bigquery table schema
    data.csv -> bigquery talbe data

Drivers
~~~~~~~

Default Google BigQuery client is used -
`docs <https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/>`__.

API Reference
-------------

Snapshot
~~~~~~~~

https://github.com/frictionlessdata/jsontableschema-py#snapshot

Detailed
~~~~~~~~

-  `Docstrings <https://github.com/frictionlessdata/jsontableschema-py/tree/master/jsontableschema/storage.py>`__
-  `Changelog <https://github.com/frictionlessdata/jsontableschema-bigquery-py/commits/master>`__

Contributing
------------

Please read the contribution guideline:

`How to Contribute <CONTRIBUTING.md>`__

Thanks!

.. |Travis| image:: https://img.shields.io/travis/frictionlessdata/jsontableschema-bigquery-py/master.svg
   :target: https://travis-ci.org/frictionlessdata/jsontableschema-bigquery-py
.. |Coveralls| image:: http://img.shields.io/coveralls/frictionlessdata/jsontableschema-bigquery-py.svg?branch=master
   :target: https://coveralls.io/r/frictionlessdata/jsontableschema-bigquery-py?branch=master
.. |PyPi| image:: https://img.shields.io/pypi/v/jsontableschema-bigquery.svg
   :target: https://pypi.python.org/pypi/jsontableschema-bigquery
.. |SemVer| image:: https://img.shields.io/badge/versions-SemVer-brightgreen.svg
   :target: http://semver.org/
.. |Gitter| image:: https://img.shields.io/gitter/room/frictionlessdata/chat.svg
   :target: https://gitter.im/frictionlessdata/chat

