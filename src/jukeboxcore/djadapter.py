"""This module provides a adapter for django to use in your tools

On import django will be setup to work. This might take 1-5 seconds! From there on you have access to the database.
If we are testing, this means the env var ``TESTING`` is set, then the import will create a test database automatically!
Creating a test db will set the env var \'TEST_DB\' to the name of the test db. When running a second instance inside
our tests, we can check if there is already a test db. If there is, use it. If not, create one.

The djadapter has shotcuts to the manger objects for each model.
To make a query, use these managers. See the documentation of
`Managers <https://docs.djangoproject.com/en/1.7/topics/db/managers/#django.db.models.Manager>`_,
`Retrieving objects <https://docs.djangoproject.com/en/1.7/topics/db/queries/#retrieving-objects>`_ and
`QuerySets <https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet>`_.
Just instead of ``<Model>.objects`` use a manager of djadapter as shortcut.

For example to query projects use::

  from jukebox.core import djadapter
  djadapter.projects.all() # returns a QuerySet that can be used similar to a list
  djadapter.projects.get(name=\'Some Project\') # returns an instance of project if
                                              # there is one but only one project with this name
  djadapter.projects.filter(semester=\'SS14\') # returns only projects of the summer semester 2014

"""
import os
import logging

import django

from jukeboxcore.log import get_logger
log = get_logger(__name__)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jukeboxcore.djsettings'
django.setup()


def setup_testdatabase():
    """Create test database

    We have to do some setup manually. ``manage.py test`` does that usually.
    Writes the db in the env var ``TEST_DB``. This can be torn down afterwards.
    When testing with nose, the fixture :func:`jukebox.tests.teardown_packagen` will do the teardown
    automatically.
    """
    # create a test db. django somehow logs a lot of debug stuff
    # because the log config does not say different
    # so we disable it for the moment
    logging.disable(logging.INFO)
    # autoclobber ignores if a test db with the same name already exists
    db = django.db.connection.creation.create_test_db(autoclobber=True)
    os.environ['TEST_DB'] = db
    logging.disable(logging.NOTSET)

# only setup a testdb if we are testing and if there isnt a test db already
if os.environ.get('TESTING', None):
    setup_testdatabase()

# now we can import the models
from jukedj import models

#==========
# Constants
#==========
GLOBAL_NAME = models.GLOBAL_NAME
"""Name for global shots and sequences"""

RNDSEQ_NAME = models.RNDSEQ_NAME
"""Name for the rnd sequence"""

DEFAULT_ASSETTYPES = [x[0] for x in models.DEFAULT_ASSETTYPES]
"""Tuples with name and description for the default assettypes that should always be available."""

DEFAULT_DEPARTMENTS = models.DEFAULT_DEPARTMENTS
"""Tuples with name, short, ordervalue and assetflag for the default departments.
Asset flag indicates if it is a department for assets or for shots.
Every project will get these departments by default.
"""

RELEASETYPES = dict((x[0], x[1][0]) for x in models.RTYP_CHOICES.items())
"""Releasetype values for the different releasetypes

the value is the actual value that will be stored in the database.
"""

FILETYPES = models.FILETYPES
"""A dict for file types that can be used in a TaskFile

the values are the actual data that gets stored in the database.

Explanations:

  :mayamainscene: probably the most common for maya scenes. these are the usual release and workfiles
                  maybe even a handoff file, if it does not need a direct subfolder.
                  Main scenes hold the main information, not just extracted parts.
                  If you export shader or maybe some blendshapes in a scene, do not use this one.
"""

#=========
# Managers
#=========

projects = models.Project.objects
"""The Project manager. Use it to query the database for projects."""

atypes = models.Atype.objects
"""The Atype manager. Use it to query the database for atypes."""

sequences = models.Sequence.objects
"""The Sequence manager. Use it to query the database for sequences."""

departments = models.Department.objects
"""The Department manager. Use it to query the database for departments."""

tasks = models.Task.objects
"""The Task manager. Use it to query the database for tasks."""

assets = models.Asset.objects
"""The Asset manager. Use it to query the database for assets."""

shots = models.Shot.objects
"""The Shot manager. Use it to query the database for shots."""

softwares = models.Software.objects
"""The Software manager. Use it to query the database for softwares."""

files = models.File.objects
"""The File manager. Use it to query the database for files."""

taskfiles = models.TaskFile.objects
"""The Taskfile manager. Use it to query the database for taskfiles."""

users = models.User.objects
"""The user manager. Use it to query the database for users."""

notes = models.Note.objects
"""The note manager. Use it to query the database for notes."""


def get_current_user():
    """Return the User instance for the currently logged in user

    :returns: user instance
    :rtype: :class:`models.User`
    :raises: DoesNotExist
    """
    return users.get(username=os.environ['USERNAME'])
