.. _database:

========
Database
========

Jukebox core depends on a PostgreSQL database.
If you do not have a configured PostgreSQL database, see section :ref:`Installing the Database <installdb>`.
If you already have an existing, configured PostgeSQL database, see section :ref:`Connect to an existing Database <connect_db>`.


.. _installdb:

---------------------------------------
Installing and Configuring the Database
---------------------------------------

To install a postgresql database, you first need postgresql itself.
Choose the right binary for your OS from `PostgreSQL Binaries <http://www.postgresql.org/download/>`_.

Start PgAdmin:

  .. figure:: ../images/pgadmin_plain.png
     :alt: pgadmin after startup.

     PgAdmin after startup. Ignore the CA-Linux-DB Server.
     You should only have a PostgreSQL Server on localhost.

It is recommended to create a new login role for all users of the new database we create.
Right click on the PostgreSQL Server and choose New Object -> New login role:

  .. figure:: ../images/pgadmin_newlogin.png
     :alt: Creating a new login role.

     Enter a name for the login role. E.g. ``jukebox_user``.

Switch to the definition tab and give this role a password:

  .. figure:: ../images/pgadmin_newloginpw.png
     :alt: Assign a password.

     Assign a new password.

Switch to the role privileges tab and check ``Can create databases``

  .. figure:: ../images/pgadmin_newloginrights.png
     :alt: Check ``Can create databases``

     Check ``Can create databases``

Then click on ``OK``.

This is your new user for the database. To create a new database, rightclick on ``Databases`` under the server and choose ``New database``:

  .. figure:: ../images/pgadmin_newdb.png
     :alt: Create a new database

     Enter Name and Owner. Owner can be the new login role you just created.

Switch to the definition tab and make user you use UTF-8 as encoding.

  .. figure:: ../images/pgadmin_definition.png
     :alt: Set encoding to UTF-8.

     Set encoding to UTF-8.

Click on ``OK``.

Now we have a new empty database! Now we have to populate the database with the tables from jukebox.
Before we can do that, you have to configure your user config to access the newly created database.
See section :ref:`Connect to an existing Database <connect_db>`.

Your PgAdmin Window should look similar to this one:

  ..figure:: ../images/pgadmin_dbadded.png
    :alt: The new database in pgadmin

    Image of the new database in PgAdmin. Note that there are no tables yet!

After you configured your user settings correctly with the information you entered in PgAdmin, go to your commandline and execute::

  jukebox manage migrate

Wait for the command to finish. Now your database is installed and configured. Congratulations!


.. _connect_db:

-------------------------------
Connect to an existing Database
-------------------------------

If you have already have a database, you have to configure your user settings, so jukebox knows which database to use.
If you have jukebox already installed, got to your commandline and execute::

  jukebox launch Configer

After a short amount of time, a window will appear. Under the jukedj section, fill in the database name, database username, password, host, port and
secret key. The secret key is a random string, which is needed by the database backend. Make sure that all users who use this database have the same secret key.

    .. figure:: ../images/configer.png
       :alt: Fill in the information under the jukedj section.

       Fill in the information under the jukedj section.

.. Warning:: The secret key and password are saved in plain text and might be a security hazard! The current implementation does not allow for anything different.
