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


@pytest.fixture(scope='function')
def notestdb(request):
    """Set an environment variable to prevent creating a test database.
    Might be necessary for subprocesses."""
    os.environ['NO_TEST_DB'] = "True"

    def fin():
        os.environ['NO_TEST_DB'] = ""
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
def prj(setup_package, prjpath):
    """Return project

    name="Pixars Plants", short='plants', _path=prjpath, semester='SS14', scale="cm"
    """
    from jukeboxcore import djadapter as dj
    return dj.projects.create(name="Pixars Plants", short='plants', _path=prjpath, semester='SS14', scale="cm")


@pytest.fixture(scope='session')
def seq(prj):
    """Return sequence

    name='Seq01', project=prj, description='plants everywhere'
    """
    from jukeboxcore import djadapter as dj
    return dj.sequences.create(name='Seq01', project=prj, description='plants everywhere')


@pytest.fixture(scope='session')
def shot(prj, seq):
    """Return shot

    name='Shot01', project=prj, sequence=seq, description='closeup of plant'
    """
    from jukeboxcore import djadapter as dj
    return dj.shots.create(name='Shot01', project=prj, sequence=seq, description='closeup of plant')


@pytest.fixture(scope='session')
def atype(prj):
    """Return assettype

    assettype is added to prj
    name='matte', description='matte paintings'
    """
    from jukeboxcore import djadapter as dj
    atype = dj.atypes.create(name='matte', description='matte paintings')
    atype.projects.add(prj)
    atype.save()
    return atype


@pytest.fixture(scope='session')
def asset(prj, atype):
    """Return asset

    project=prj, atype=atype, name='piranha plant', description='eats mario'
    """
    from jukeboxcore import djadapter as dj
    return dj.assets.create(project=prj, atype=atype, name='piranha plant', description='eats mario')


@pytest.fixture(scope='session')
def dep1(setup_package):
    """Return a department

    name="Design", short="des", assetflag=False
    """
    from jukeboxcore import djadapter as dj
    return dj.departments.create(name="Design", short="des", assetflag=False)


@pytest.fixture(scope='session')
def dep2(setup_package):
    """Return a department

    name="Destruction", short="buum", assetflag=False
    """
    from jukeboxcore import djadapter as dj
    return dj.departments.create(name="Destruction", short="buum", assetflag=False)


@pytest.fixture(scope='session')
def dep3(setup_package):
    """Return a department

    name="Matte", short="matte", assetflag=True
    """
    from jukeboxcore import djadapter as dj
    return dj.departments.create(name="Matte", short="matte", assetflag=True)


@pytest.fixture(scope='session')
def task1(prj, shot, dep1):
    """Return task

    department=dep1, project=prj, status='New', element=shot
    """
    from jukeboxcore import djadapter as dj
    return dj.tasks.create(department=dep1, project=prj, status='New', element=shot)


@pytest.fixture(scope='session')
def task2(prj, shot, dep2):
    """Return task

    department=dep2, project=prj, status='New', element=shot
    """
    from jukeboxcore import djadapter as dj
    return dj.tasks.create(department=dep2, project=prj, status='New', element=shot)


@pytest.fixture(scope='session')
def task3(prj, asset, dep3):
    from jukeboxcore import djadapter as dj
    return dj.tasks.create(department=dep3, project=prj, status='New', element=asset)


@pytest.fixture(scope='session')
def tfile(task1, user):
    """Return taskfile

    task=task1, version=5, releasetype='handoff', path='anicepath', user=user, typ=dj.FILETYPES['mayamainscene']
    """
    from jukeboxcore import djadapter as dj
    return dj.taskfiles.create(task=task1, version=5, releasetype='handoff', path='anicepath', user=user, typ=dj.FILETYPES['mayamainscene'])


@pytest.fixture(scope='session')
def taskfileinfo(tfile):
    """Return a TaskFileInfo for the Taskfile of the taskfile fixture

    task=task1, version=5, releasetype='handoff', user=user, typ=dj.FILETYPES['mayamainscene'], descriptor="desc1"
    """
    return TaskFileInfo(task=tfile.task,
                        version=tfile.version,
                        releasetype=tfile.releasetype,
                        typ=tfile.typ,
                        descriptor="desc1")


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
