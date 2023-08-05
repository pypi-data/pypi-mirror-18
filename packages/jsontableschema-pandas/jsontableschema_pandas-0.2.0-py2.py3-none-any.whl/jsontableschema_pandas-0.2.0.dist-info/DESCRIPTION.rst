jsontableschema-pandas
======================

| |Travis|
| |Coveralls|
| |PyPi|
| |SemVer|
| |Gitter|

Generate and load Pandas data frames based on JSON Table Schema
descriptors.

    Version ``v0.2`` contains breaking changes:

-  removed ``Storage(prefix=)`` argument (was a stub)
-  renamed ``Storage(tables=)`` to ``Storage(dataframes=)``
-  renamed ``Storage.tables`` to ``Storage.buckets``
-  changed ``Storage.read`` to read into memory
-  added ``Storage.iter`` to yield row by row

Getting Started
---------------

Installation
~~~~~~~~~~~~

::

    $ pip install datapackage
    $ pip install jsontableschema-pandas

Example
~~~~~~~

You can easily load resources from a data package as Pandas data frames
by simply using ``datapackage.push_datapackage`` function:

.. code:: python

    >>> import datapackage

    >>> data_url = 'http://data.okfn.org/data/core/country-list/datapackage.json'
    >>> storage = datapackage.push_datapackage(data_url, 'pandas')

    >>> storage.buckets
    ['data___data']

    >>> type(storage['data___data'])
    <class 'pandas.core.frame.DataFrame'>

    >>> storage['data___data'].head()
                 Name Code
    0     Afghanistan   AF
    1   Åland Islands   AX
    2         Albania   AL
    3         Algeria   DZ
    4  American Samoa   AS

Also it is possible to pull your existing data frame into a data
package:

.. code:: python

    >>> datapackage.pull_datapackage('/tmp/datapackage.json', 'country_list', 'pandas', tables={
    ...     'data': storage['data___data'],
    ... })
    Storage

Storage
~~~~~~~

Package implements `Tabular
Storage <https://github.com/frictionlessdata/jsontableschema-py#storage>`__
interface.

We can get storage this way:

.. code:: python

    >>> from jsontableschema_pandas import Storage

    >>> storage = Storage()

Storage works as a container for Pandas data frames. You can define new
data frame inside storage using ``storage.create`` method:

.. code:: python

    >>> storage.create('data', {
    ...     'primaryKey': 'id',
    ...     'fields': [
    ...         {'name': 'id', 'type': 'integer'},
    ...         {'name': 'comment', 'type': 'string'},
    ...     ]
    ... })

    >>> storage.buckets
    ['data']

    >>> storage['data'].shape
    (0, 0)

Use ``storage.write`` to populate data frame with data:

.. code:: python

    >>> storage.write('data', [(1, 'a'), (2, 'b')])

    >>> storage['data']
    id comment
    1        a
    2        b

Also you can use
`tabulator <https://github.com/frictionlessdata/tabulator-py>`__ to
populate data frame from external data file:

.. code:: python

    >>> import tabulator

    >>> with tabulator.Stream('data/comments.csv', headers=1) as stream:
    ...     storage.write('data', stream)

    >>> storage['data']
    id comment
    1        a
    2        b
    1     good

As you see, subsequent writes simply appends new data on top of existing
ones.

API Reference
-------------

Snapshot
~~~~~~~~

https://github.com/frictionlessdata/jsontableschema-py#snapshot

Detailed
~~~~~~~~

-  `Docstrings <https://github.com/frictionlessdata/jsontableschema-py/tree/master/jsontableschema/storage.py>`__
-  `Changelog <https://github.com/frictionlessdata/jsontableschema-pandas-py/commits/master>`__

Contributing
------------

Please read the contribution guideline:

`How to Contribute <CONTRIBUTING.md>`__

Thanks!

.. |Travis| image:: https://img.shields.io/travis/frictionlessdata/jsontableschema-pandas-py/master.svg
   :target: https://travis-ci.org/frictionlessdata/jsontableschema-pandas-py
.. |Coveralls| image:: http://img.shields.io/coveralls/frictionlessdata/jsontableschema-pandas-py.svg?branch=master
   :target: https://coveralls.io/r/frictionlessdata/jsontableschema-pandas-py?branch=master
.. |PyPi| image:: https://img.shields.io/pypi/v/jsontableschema-pandas.svg
   :target: https://pypi.python.org/pypi/jsontableschema-pandas
.. |SemVer| image:: https://img.shields.io/badge/versions-SemVer-brightgreen.svg
   :target: http://semver.org/
.. |Gitter| image:: https://img.shields.io/gitter/room/frictionlessdata/chat.svg
   :target: https://gitter.im/frictionlessdata/chat

