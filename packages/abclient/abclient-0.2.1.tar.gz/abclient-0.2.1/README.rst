abclient: Python library for EISOO AnyBackup APIs
=================================================

.. image:: https://img.shields.io/pypi/v/abclient.svg
    :target: https://pypi.python.org/pypi/abclient/


**abclient** is a client library for EISOO AnyBackup APIs.

**abclient** allows openstack-karbor to create backups for databases and filesystems.


Installation
------------

To install abclient, simply:

.. code-block:: bash

    $ pip install abclient

How to use
-----------

.. code-block:: python

    >>>from abclient import backup_manager
    >>>ab = backup_manager.eisooBackupManager('IP_ADDR','MACHINE_CODE')
    >>>ab.start_backup(...)

API Support
---------------

- Create backup for ORACLE Database

more API will be supported in the future.


License
-------

Apache License Version 2.0 http://www.apache.org/licenses/LICENSE-2.0
