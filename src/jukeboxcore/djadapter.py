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
import django.conf

from jukeboxcore.log import get_logger
log = get_logger(__name__)
import jukedj.settings
from jukeboxcore.constants import DJSETTINGS, TEST_PROJECTS_DIR

#TODO
# SETUP DJANGO
os.environ['DJANGO_SETTINGS_MODULE'] = DJSETTINGS
# if we are testing, and there is already a test db, use it as default
# this is the case when we run a second python instance inside our tests
# e.g. mayatests
if os.environ.get('TEST_DB', False):
    jukedj.settings.DATABASES['default']['NAME'] = os.environ['TEST_DB']
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
if os.environ.get('TESTING', None) and not os.environ.get('TEST_DB', False):
    setup_testdatabase()

# now we can import the models
from muke import models
from muke import validators

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


#TODO put in test
def populate():
    """Populate the database with some data

    :returns: None
    :rtype: None
    :raises: None
    """
    from jukebox.core.filesys import JB_File, TaskFileInfo
    usr = users.create_user(username=os.environ['USERNAME'])

    prj1 = projects.create(name="Dancing with Smurfs", short='dws', _path=os.path.join(TEST_PROJECTS_DIR, 'dws'), semester='SS14',
                                      framerate=25, resx=1920, resy=1080, scale='cm', status='New')
    prj1.users.add(usr)
    prj1.save()
    prj2 = projects.create(name="Avatar 3", short='avt3', _path=os.path.join(TEST_PROJECTS_DIR, 'avatar3'), semester='WS14/15')
    prj2.users.add(usr)
    prj2.save()
    prj3 = projects.create(name="RipOff Remake", short='ror', _path=os.path.join(TEST_PROJECTS_DIR, 'ror'), semester='SS14')
    prj3.users.add(usr)
    prj3.save()

    laydep = departments.create(name='Layout', short='lay', assetflag=False)
    desdep = departments.create(name='Design', short='des', assetflag=True)
    laydep.projects.add(prj1)
    laydep.save()
    desdep.projects.add(prj1)
    desdep.save()

    for p in [prj1, prj2, prj3]:
        seq1 = sequences.create(name='Seq01', project=p, description='%s main seq' % p.name)
        seq2 = sequences.create(name='Seq02', project=p, description='%s secondary seq' % p.name)

        for seq in [seq1, seq2]:
            s1 = shots.create(name='Shot01', project=p, description='Awesomeshot of %s' % seq.name, sequence=seq)
            s2 = shots.create(name='Shot02', project=p, description='crappy %ss shot' % seq.name, sequence=seq)
            s3 = shots.create(name='Shot03', project=p, description='slighlty cooler shot of %s' % seq.name, sequence=seq)
            for s in [s1, s2, s3]:
                for t in s.tasks.all():
                    for i in range(5):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['work'],
                                           typ=models.FILETYPES['mayamainscene'], descriptor='take1')
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ, descriptor=tfi.descriptor)
                    for i in range(3):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['release'],
                                           typ=models.FILETYPES['mayamainscene'])
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ, descriptor=tfi.descriptor)
                    for i in range(4):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['handoff'],
                                           typ=models.FILETYPES['mayamainscene'])
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ, descriptor=tfi.descriptor)

        for at in p.atype_set.all():
            asset1 = assets.create(name='Asset01', project=p, atype=at, description="description for Asset01")
            asset2 = assets.create(name='Asset20', project=p, atype=at, description="description for Asset20")
            asset3 = assets.create(name='Asset3', project=p, atype=at, description="description for Asset3")
            for a in [asset1, asset2, asset3]:
                for t in a.tasks.all():
                    for i in range(3):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['work'],
                                           typ=models.FILETYPES['mayamainscene'], descriptor='take1')
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ, descriptor=tfi.descriptor)
                    for i in range(5):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['release'],
                                                    typ=models.FILETYPES['mayamainscene'])
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ)
                    for i in range(4):
                        tfi = TaskFileInfo.get_next(t, releasetype=RELEASETYPES['handoff'],
                                                    typ=models.FILETYPES['mayamainscene'])
                        jbfile = JB_File(tfi)
                        path = jbfile.get_fullpath()
                        taskfiles.create(user=usr, task=t, version=tfi.version,
                                         releasetype=tfi.releasetype, path=path,
                                         typ=tfi.typ)
