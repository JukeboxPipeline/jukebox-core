import os
import getpass
import tempfile

import pytest
import django

from jukeboxcore.action import ActionStatus
from jukeboxcore.filesys import TaskFileInfo
from PySide import QtGui


@pytest.fixture(scope='session', autouse=True)
def setup_package(request):
    os.environ['JUKEBOX_TESTING'] = 'True'
    # create a QtGui Application just in case a module needs it.
    if QtGui.qApp is None:
        QtGui.QApplication([], QtGui.QApplication.GuiClient)

    def fin():
        test_db = os.environ.get('TEST_DB', None)
        if test_db:
            django.db.connection.creation.destroy_test_db(test_db)
    request.addfinalizer(fin)


@pytest.fixture(scope='session')
def user(setup_package):
    from jukeboxcore.djadapter import users
    name = getpass.getuser()
    return users.create_user(username=name)


@pytest.fixture(scope='session')
def prjpath():
    """Return a path for the project of the prj fixture"""
    return os.path.join(tempfile.gettempdir(), "testpixarplants")


class DjangoProjectContainer(object):
    """A container that holds a all
    projects, sequences, shots, assettypes, assets, tasks and taskfiles.
    """

    def __init__(self, ):
        """
        :raises: None
        """
        self.prjs = []
        self.sequences = []
        self.shots = []
        self.atypes = []
        self.asset = []
        self.shotdepartments = []
        self.assetdepartments = []
        self.shottasks = []
        self.assettasks = []
        self.assettaskfiles = []
        self.shottaskfiles = []
        self.assettfis = []
        self.shottfis = []


@pytest.fixture(scope='session')
def djprj(setup_package, prjpath):
    from jukeboxcore import djadapter as dj
    c = DjangoProjectContainer()
    prj = dj.projects.create(name="Pixars Plants", short='plants', _path=prjpath, semester='SS14', scale="cm")
    c.prjs.append(prj)

    seqparams = [{'name': 'Seq01', 'description': 'plants everywhere'},
                 {'name': 'Seq02', 'description': 'little less plants'}]
    shotparams = [{'name': 'Shot01', 'description': 'closeup of plant'},
                  {'name': 'Shot02', 'description': 'roots of plant'}]
    atypeparams = [{'name': 'matte', 'description': 'matte paintings'},
                   {'name': 'char', 'description': 'character'}]
    assetparams = [{'name': 'piranha plant', 'description': 'eats mario'},
                   {'name': 'mario', 'description': 'stomps plants'}]
    adepparams = [{'name': 'Matte', 'short': 'matte'},
                  {'name': 'Modeling', 'short': 'mod'}]
    sdepparams = [{'name': 'Design', 'short': 'des'},
                  {'name': 'Destruction', 'short': 'buum'}]
    stfparams = [{'version': 1, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 2, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 3, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 1, 'releasetype': 'work', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': 'desc1'}]
    atfparams = [{'version': 1, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 2, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 3, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 1, 'releasetype': 'work', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': 'desc1'}]

    for adepparam in adepparams:
        dep = dj.departments.create(assetflag=True, **adepparam)
        c.assetdepartments.append(dep)
    for sdepparam in sdepparams:
        dep = dj.departments.create(assetflag=False, **sdepparam)
        c.shotdepartments.append(dep)

    for seqparam in seqparams:
        seq = dj.sequences.create(project=prj, **seqparam)
        c.sequences.append(seq)
        for shotparam in shotparams:
            shot = dj.shots.create(project=prj, **shotparam)
            c.shots.append(shot)

    for atypeparam in atypeparams:
        atype = dj.atype.create(**atypeparam)
        atype.projects.add(prj)
        atype.save()
        c.atypes.append(atype)
        for assetparam in assetparams:
            asset = dj.assets.create(project=prj, atype=atype, **assetparam)
            c.assets.append(asset)

    for dep in c.shotdepartments:
        for s in c.shots:
            task = dj.tasks.create(department=dep, project=prj, status='New', element=s)
            c.shottasks.append(task)
            for stfparam in stfparams:
                tfile = dj.taskfiles.create(task=task,
                                            user=user,
                                            path="%s%s%s%s" % (prj.name, dep.short, stfparam['releasetype'], stfparam['version']),
                                            **stfparam)
                c.shottaskfiles.append(tfile)
                tfileinfo = TaskFileInfo(task=tfile.task,
                                         version=tfile.version,
                                         releasetype=tfile.releasetype,
                                         typ=tfile.typ,
                                         descriptor=tfile.descriptor)
                c.shottfis.append(tfileinfo)
    for dep in c.assetdepartments:
        for a in c.assets:
            task = dj.tasks.create(department=dep, project=prj, status='New', element=a)
            c.assettasks.append(task)
            for atfparam in atfparams:
                tfile = dj.taskfiles.create(task=task,
                                            user=user,
                                            path="%s%s%s%s" % (prj.name, dep.short, atfparam['releasetype'], atfparam['version']),
                                            **atfparam)
                c.assettaskfiles.append(tfile)
                tfileinfo = TaskFileInfo(task=tfile.task,
                                         version=tfile.version,
                                         releasetype=tfile.releasetype,
                                         typ=tfile.typ,
                                         descriptor=tfile.descriptor)
                c.assettfis.append(tfileinfo)

    # TODO link asset and shots


@pytest.fixture(scope='session')
def successf():
    """Return a function that will return a successful action status"""
    def func(f):
        return ActionStatus(ActionStatus.SUCCESS, "Success")
    return func


@pytest.fixture(scope='session')
def errorf():
    """Return a function that will raise an exception"""
    def func(f):
        raise Exception
    return func


@pytest.fixture(scope='session')
def failf():
    """Return a function that will return a failed action status"""
    def func(f):
        return ActionStatus(ActionStatus.FAILURE, "Failed")
    return func
