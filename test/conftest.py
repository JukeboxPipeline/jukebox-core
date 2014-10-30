import os
import getpass

import pytest
import django


@pytest.fixture(scope='session', autouse=True)
def setup_package(request):
    os.environ['JUKEBOX_TESTING'] = 'True'

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
def dummyproject(request, setup_package):
    """Returns:

    project: name="Pixars Plants", short='plants', _path='plantpath', semester='SS14'
    sequence: name='Seq01'
    shot: name='Shot01'
    department1: name="Design", short="des", assetflag=False
    department2: name="Destruction", short="buum", assetflag=False
    task1: task for shot and department1, status new
    task2: task for shot and department2, status new
    user: Uz
    taskfile: task=task1, version=5, releasetype='handoff', path='anicepath', user=usrer, typ=dj.FILETYPES['mayamainscene']
    assettype: name='matte', description='matte paintings'
    asset: name='piranha plant', description='eats mario'
    """
    from jukeboxcore import djadapter as dj
    prj = dj.projects.create(name="Pixars Plants", short='plants', _path='plantpath', semester='SS14', scale="cm")
    seq = dj.sequences.create(name='Seq01', project=prj, description='plants everywhere')
    shot = dj.shots.create(name='Shot01', project=prj, sequence=seq, description='closeup of plant')
    dep1 = dj.departments.create(name="Design", short="des", assetflag=False)
    dep2 = dj.departments.create(name="Destruction", short="buum", assetflag=False)
    task1 = dj.tasks.create(department=dep1, project=prj, status='New', element=shot)
    task2 = dj.tasks.create(department=dep2, project=prj, status='New', element=shot)
    usr = dj.users.create_user(username='Uz')
    tfile = dj.taskfiles.create(task=task1, version=5, releasetype='handoff', path='anicepath', user=usr, typ=dj.FILETYPES['mayamainscene'])
    atype = dj.atypes.create(name='matte', description='matte paintings')
    atype.projects.add(prj)
    atype.save()
    asset = dj.assets.create(project=prj, atype=atype, name='piranha plant', description='eats mario')

    l = (prj, seq, shot, dep1, dep2, task1, task2, usr, tfile, atype, asset)
    return l
