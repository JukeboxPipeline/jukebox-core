import os
import getpass
import tempfile

import pytest
import django

from jukeboxcore.action import ActionStatus
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
