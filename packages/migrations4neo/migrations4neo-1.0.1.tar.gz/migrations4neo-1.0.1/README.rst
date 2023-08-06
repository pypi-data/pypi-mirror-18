==============
migrations4neo
==============
:Info: Easy migrations for neo4j 
:Repository: https://github.com/turkus/migrations4neo
:Author: Wojciech Rola 
:Maintainer: Wojciech Rola 

How to start?
-------------

We need to create basics:

.. code-block:: console

    mig4neo init mig4neo

It will create mig4neo folder and subfolder called versions, where your migrations will land.

Then you have to edit mig4neo.ini according your needs:
<path to your project dir>/mig4neo.ini

What's next?
------------

Create revision:

.. code-block:: console

    mig4neo revision -m 'This is my revision'
  


Adjust it by editing revision's file (*.py).

Make it happen
--------------

Upgrade db:

.. code-block:: console

    mig4neo upgrade --revisions 4asvg34,3fadg4

You can also downgrade:

.. code-block:: console

    mig4neo downgrade --revisions 4asvg34,3fadg4e
