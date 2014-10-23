"""This module provides a adapter for django to use in your tools

On import django will be setup to work. This might take 1-5 seconds! From there on you have access to the database.
If we are testing, this means the env var ``JUKEBOX_TESTING`` is set, then the import will create a test database automatically!
Creating a test db will set the env var \'TEST_DB\' to the name of the test db, so we can destroy it later.

The djadapter has shotcuts to the manger objects for each model.
To make a query, use these managers. See the documentation of
`Managers <https://docs.djangoproject.com/en/1.7/topics/db/managers/#django.db.models.Manager>`_,
`Retrieving objects <https://docs.djangoproject.com/en/1.7/topics/db/queries/#retrieving-objects>`_ and
`QuerySets <https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet>`_.
Just instead of ``<Model>.objects`` use a manager of djadapter as shortcut.

For example to query projects use::

  from jukeboxcore import djadapter
  djadapter.projects.all() # returns a QuerySet that can be used similar to a list
  djadapter.projects.get(name=\'Some Project\') # returns an instance of project if
                                              # there is one but only one project with this name
  djadapter.projects.filter(semester=\'SS14\') # returns only projects of the summer semester 2014

"""
import os
import logging
import getpass

import django

from jukeboxcore.log import get_logger
log = get_logger(__name__)

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
   import jukeboxcore.main
   jukeboxcore.main.init_environment()

django.setup()


def setup_testdatabase():
    """Create test database

    We have to do some setup manually. ``manage.py test`` does that usually.
    Writes the db in the env var ``TEST_DB``. This can be torn down afterwards.
    """
    # create a test db. django somehow logs a lot of debug stuff
    # because the log config does not say different
    # so we disable it for the moment
    from django.conf import settings
    logging.disable(logging.INFO)
    # autoclobber ignores if a test db with the same name already exists
    django.db.connection.creation.create_test_db(autoclobber=False)
    os.environ['TEST_DB'] = settings.DATABASES['default']['NAME']
    logging.disable(logging.NOTSET)

# only setup a testdb if we are testing and if there isnt a test db already
if os.environ.get('JUKEBOX_TESTING', None):
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

RELEASETYPES = {
    'release': 'release',
    'work': 'work',
    'handoff': 'handoff',
}
"""Releasetype values for the different releasetypes

the values consist of tuples with the actual name and a description.
"""

FILETYPES = {
    'mayamainscene': 'mayamainscene'
}
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
    name = getpass.getuser()
    return users.get(username=name)
