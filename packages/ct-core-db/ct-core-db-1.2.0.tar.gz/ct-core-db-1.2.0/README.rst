CT Core DB
###########

.. _description:

CT Core DB -- Catalant Core DB Framework.

The main features available in this framework include:

- The **SQLAlchemy** toolkit with our customizations and enhancements
- Commands for versioning and managing **MySQL** database schemas
- Debugging and development utilities for working with SQLAlchemy queries and events

.. _documentation:

`SQLAlchemy Documentation`_

.. _`SQLAlchemy Documentation`: http://http://www.sqlalchemy.org/

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 2.6
- mysql-diff == 0.3 (built into the base Docker image)

.. _installation:

Installation
=============

**CT Core DB** is hosted on our internal `PyPi repository`_. It should be installed using pip::

    pip install ct-core-db

.. _PyPi repository: https://devpi.gocatalant.com/catalant/prod/ct-core-db

.. _usage:

Usage
=====

Most of the functionality exposed by this library is made available through the SQLAlchemy
``ct_core_db.db`` instance or via the ``db`` Flask commands in ct-core-api_.

.. _ct-core-api: https://github.com/Catalant/ct-core-api

SQLAlchemy Enhancements
```````````````````````
- ``ct_core_db.lib.db_utils`` -- Various utilities for debugging and logging SQLAlchemy queries and events
- ``ct_core_db.lib.sqla`` -- Improved signalling session that avoids PK collisions, base model, and model mixins
- ``ct_core_db.lib.sqla_types`` -- Custom SQLAlchemy column data types

MySQL Diff
``````````
Use the ``mysql_diff.MySQLDiffCommand`` to produce a database migration script based on the differences between two
MySQL database schemas::

    from ct_core_db.lib import mysql_diff

    mysql_diff_cmd = mysql_diff.MySQLDiffCommand()
    diff_output = mysql_diff_cmd('jdbc_db_url_a', 'jdbc_db_url_b')

MySQL Version Manager
`````````````````````
Use the ``mysql_version.MySQLVersionManager`` class to create, diff, and upgrade your MySQL database schemas::

    from ct_core_db.lib import mysql_diff

    mysql_version_manager = mysql_version.MySQLVersionManager(engine, mysql_diff_cmd)
    mysql_version_manager.init_db()
    mysql_version_manager.create_db()
    mysql_version_manager.diff_db()  # Invokes `mysql_diff_command`
    mysql_version_manager.upgrade_db()

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/catalant/ct-core-db/issues

.. _contributing:

Contributing
============

Development of ct-core-db happens at github: https://github.com/catalant/ct-core-db


Contributors
=============

* jcrafford_ (Justin Crafford)

.. _license:

License
=======

Licensed under a `MIT license`_.

.. _links:

.. _MIT license: https://opensource.org/licenses/MIT
.. _jcrafford: https://github.com/jcrafford
