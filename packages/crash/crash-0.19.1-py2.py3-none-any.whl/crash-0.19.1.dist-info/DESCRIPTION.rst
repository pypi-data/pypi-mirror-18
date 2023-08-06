.. image:: https://cdn.crate.io/web/2.0/img/crate-logo_330x72.png
   :width: 165px
   :height: 36px
   :alt: Crate.IO
   :target: https://crate.io

|

.. image:: https://travis-ci.org/crate/crash.svg?branch=master
        :target: https://travis-ci.org/crate/crash
        :alt: Test

.. image:: https://badge.fury.io/py/crash.png
    :target: http://badge.fury.io/py/crash
    :alt: Version

.. image:: https://pypip.in/download/crash/badge.png
    :target: https://pypi.python.org/pypi/crash/
    :alt: Downloads

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://crate.io/docs/reference/crash/

.. image:: https://img.shields.io/pypi/pyversions/crash.svg
   :target: https://pypi.python.org/pypi/crash/
   :alt: Python Version


========
Overview
========

This is the Crate shell called ``crash``.

Installation
============

Installing via pip
------------------

To install crash via `pip <https://pypi.python.org/pypi/pip>`_ use
the following command::

    $ pip install crash

To update use::

    $ pip install -U crash

Standalone
----------

There is also a single file executable that includes all dependencies and can
be run as long as python (>= 2.7) is available on the system.

`Download Crash bundle
<https://cdn.crate.io/downloads/releases/crash_standalone_latest>`_

The bundle can then be executed using python::

    python ./crash_standalone_latest

Or::

    chmod +x ./crash_standalone_latest
    ./crash_standalone_latest


Crash supported Python 2.6 until 0.16. `Use Crash 0.16.0
<https://cdn.crate.io/downloads/releases/crash_standalone_0.16.0>`_ if you're
running Python 2.6

Usage
-----

If the package was installed using `pip` the shell can be started by
running the command `crash` in a terminal.

For usage information and command line options invoke::

    crash --help

Or consult the `crash documentation 📚 <https://crate.io/docs/reference/crash/>`_.

Are you a Developer?
====================

You can build Crash on your own with the latest version hosted on GitHub.
To do so, please refer to ``DEVELOP.rst`` for further information.

Help & Contact
==============

Do you have any questions? Or suggestions? We would be very happy
to help you. So, feel free to swing by our Community on Slack_.
Or for further information and official contact please
visit `https://crate.io/ <https://crate.io/>`_.

.. _Slack: https://crate.io/docs/support/slackin/

License
=======

Copyright 2013-2014 CRATE Technology GmbH ("Crate")

Licensed to CRATE Technology GmbH ("Crate") under one or more contributor
license agreements.  See the NOTICE file distributed with this work for
additional information regarding copyright ownership.  Crate licenses
this file to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.  You may
obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
License for the specific language governing permissions and limitations
under the License.

However, if you have executed another commercial license agreement
with Crate these terms will supersede the license and you may use the
software solely pursuant to the terms of the relevant commercial agreement.

====================
Installation & Usage
====================

If the package was installed using ``pip`` the shell can be started by
invoking ``crash`` in a terminal. We recommend to install it to the Python
user install directory to avoid unwanted dependency conflicts.

::

    pip install --user crash


.. note::
    If ``crash`` is installed in the Python user install directory please ensure
    that ``~/.local/bin`` (Linux), or ``%APPDATA%\Python\<version>\Scripts``
    (Windows) is added to the system path.

``crash`` by default will try to connect to ``localhost:4200``. To connect to
another host use the ``connect`` command inside the shell or use the ``--hosts``
argument when launching the shell.

``crash`` started with the ``-v`` switch (once or more times) will log useful information
when it comes to debugging, like what connection attempts are made and full tracebacks
of server errors.

For more information about the available command line arguments see `Command Line Arguments`_.

When you connect to a server that is not reachable or whose hostname cannot be resolved
you will get an error::

    cr> \connect 127.0.0.1:65535
    +------------------------+-----------+---------+-----------+-----------...-+
    | server_url             | node_name | version | connected | message       |
    +------------------------+-----------+---------+-----------+-----------...-+
    | http://127.0.0.1:65535 |      NULL | 0.0.0   | FALSE     | Server not... |
    +------------------------+-----------+---------+-----------+-----------...-+
    CONNECT ERROR

::

    cr> \connect 300.300.300.300:4200
    +-----------------------------+-----------+---------+-----------+-------------...-+
    | server_url                  | node_name | version | connected | message         |
    +-----------------------------+-----------+---------+-----------+-------------...-+
    | http://300.300.300.300:4200 |      NULL | 0.0.0   | FALSE     | Server not a... |
    +-----------------------------+-----------+---------+-----------+-------------...-+
    CONNECT ERROR

Successful connects will give you some information about the servers you connect to::

    cr> \connect 127.0.0.1:44209;
    +------------------------+-----------+---------+-----------+---------+
    | server_url             | node_name | version | connected | message |
    +------------------------+-----------+---------+-----------+---------+
    | http://127.0.0.1:44209 | crate     | ...     | TRUE      | OK      |
    +------------------------+-----------+---------+-----------+---------+
    CONNECT OKCLUSTER CHECK OKCrate ... does not support the "\check nodes" command.

If you connect to more than one server, the command will succeed
if at least one server is reachable::

    cr> \connect 127.0.0.1:44209 300.300.300.300:4295;
    +-----------------------------+-----------+---------+-----------+-----------...-+
    | server_url                  | node_name | version | connected | message       |
    +-----------------------------+-----------+---------+-----------+-----------...-+
    | http://127.0.0.1:44209      | crate     | ...     | TRUE      | OK            |
    | http://300.300.300.300:4295 | NULL      | 0.0.0   | FALSE     | Server not... |
    +-----------------------------+-----------+---------+-----------+-----------...-+
    CONNECT OKCLUSTER CHECK OKCrate ... does not support the "\check nodes" command.

Once the shell is connected, SQL statements can be executed simply by entering
them without any special arguments like this::

    cr> SELECT schema_name, table_name FROM information_schema.tables
    ... ORDER BY table_name;
    +--------------------+-------------------+
    | schema_name        | table_name        |
    +--------------------+-------------------+
    | sys                | checks            |
    | sys                | cluster           |
    | information_schema | columns           |
    | sys                | jobs              |
    | sys                | jobs_log          |
    | sys                | nodes             |
    | sys                | operations        |
    | sys                | operations_log    |
    | sys                | repositories      |
    | information_schema | routines          |
    | information_schema | schemata          |
    | sys                | shards            |
    | sys                | snapshots         |
    | information_schema | table_constraints |
    | information_schema | table_partitions  |
    | information_schema | tables            |
    +--------------------+-------------------+
    SELECT 16 rows in set (... sec)

When the Crate shell is started with the option ``-v`` debugging information will be printed::

    cr> select x from y;
    SQLActionException[TableUnknownException: Table 'doc.y' unknown]
    ...



Limitations
===========

Nested Objects and Arrays
-------------------------

.. note::

    Since crate 0.39.0 it is possible to use object and array literals and the
    limitation does not apply when connecting to a crate instance running > 0.39.0.

While it is possible to select or filter by nested objects it is currently not
possible to insert them using crash. In order to do that the `Crate REST
endpoint`_ or a client library like `crate-python`_ has to be used.

The same also applies for arrays.

.. _`Crate REST Endpoint`: https://crate.io/docs/current/sql/rest.html
.. _`Command Line Arguments`: https://crate.io/docs/projects/crash/en/stable/cli.html
.. _`crate-python`: https://pypi.python.org/pypi/crate/


