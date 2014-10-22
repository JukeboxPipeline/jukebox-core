============
Installation
============

It is recommended to use python 2.7 64-bit.

Install jukebox-core via pip or easy-install. Pip is recommended::

    $ pip install jukebox-core
    $ easy_install jukebox-core

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv jukebox-core
    $ pip install jukebox-core

-------
Windows
-------

Jukebox Core has a psycopg dependency that might not be able to be installed via pip.
So before you install jukebox-core download the binary from `Psycopg2 for Windows <http://www.stickpeople.com/projects/python/win-psycopg/>`_ and install it via::

  easy_install path/to/downloadedbinary.exe

I recommend the python 2.7 64-bit version.


-----
Linux
-----

Jukebox Core has a psycopg dependency that might not be able to be installed via pip. Check this `Guide <http://initd.org/psycopg/docs/install.html>`_ on how to install psycopg on linux.
On Debian, Ubuntu and other deb-based distributions you should just need::

  sudo apt-get install python-psycopg2
