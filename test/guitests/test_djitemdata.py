from datetime import datetime

from nose.tools import eq_
from PySide import QtCore

from jukeboxcore.gui import djitemdata
from jukeboxcore import djadapter as dj
from jukeboxcore.gui.main import dt_to_qdatetime

prj = None
seq = None
shot = None
task = None
tfile = None
atype = None
asset = None
usr = None
dep = None
dr = QtCore.Qt.DisplayRole
er = QtCore.Qt.EditRole


def setup_module():
    global usr, prj, seq, shot, task, tfile, atype, asset, dep
    dj.projects.all().delete()  # just to be sure
    prj = dj.projects.create(name="Pixars Plants", short='plants', _path='plantpath', semester='SS14',
                            framerate=25, resx=1920, resy=1080, scale='cm', status='New')
    seq = dj.sequences.create(name='Seq01', project=prj, description='plants everywhere')
    shot = dj.shots.create(name='Shot01', project=prj, sequence=seq, description='closeup of plant', startframe=1, endframe=50, handlesize=8)
    dep = dj.departments.create(name='Design', short='des', assetflag=False)
    task = dj.tasks.create(department=dep, project=prj, status='New', element=shot)
    usr = dj.users.create_user(username='Uz')
    tfile = dj.taskfiles.create(task=task, version=5, releasetype='handoff', path='anicepath', user=usr, typ=dj.FILETYPES['mayamainscene'])
    atype = dj.atypes.create(name='matte', description='matte paintings')
    atype.projects.add(prj)
    atype.save()
    asset = dj.assets.create(project=prj, atype=atype, name='piranha plant', description='eats mario')


def teardown_module():
    prj.delete()
    atype.delete()
    usr.delete()
    dep.delete()


def test_prj_name_data():
    eq_(djitemdata.prj_name_data(prj, dr), "Pixars Plants")


def test_prj_short_data():
    eq_(djitemdata.prj_short_data(prj, dr), "plants")


def test_prj_path_data():
    eq_(djitemdata.prj_path_data(prj, dr), "plantpath")


def test_prj_created_data():
    now = datetime.now()
    prj.date_created = now
    eq_(djitemdata.prj_created_data(prj, dr), now.isoformat(" "))


def test_prj_semester_data():
    eq_(djitemdata.prj_semester_data(prj, dr), "SS14")


def test_prj_fps_data():
    eq_(djitemdata.prj_fps_data(prj, dr), "25")


def test_prj_resolution_data():
    eq_(djitemdata.prj_resolution_data(prj, dr), "1920 x 1080")


def test_prj_scale_data():
    eq_(djitemdata.prj_scale_data(prj, dr), "cm")


def test_prj_status_data():
    eq_(djitemdata.prj_status_data(prj, dr), "New")


class Test_ProjectItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.ProjectItemData(prj)

    def test_column_count(self):
        eq_(self.idata.column_count(), 9)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "Pixars Plants")
        eq_(self.idata.data(1, dr), "plants")


def test_seq_name_data():
    eq_(djitemdata.seq_name_data(seq, dr), "Seq01")


def test_seq_description_data():
    eq_(djitemdata.seq_description_data(seq, dr), "plants everywhere")


class Test_SequenceItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.SequenceItemData(seq)

    def test_column_count(self):
        eq_(self.idata.column_count(), 2)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "Seq01")
        eq_(self.idata.data(1, dr), "plants everywhere")


def test_shot_name_data():
    eq_(djitemdata.shot_name_data(shot, dr), 'Shot01')


def test_shot_description_data():
    eq_(djitemdata.shot_description_data(shot, dr), 'closeup of plant')


def test_shot_duration_data():
    eq_(djitemdata.shot_duration_data(shot, dr), '50')


def test_shot_start_data():
    eq_(djitemdata.shot_start_data(shot, dr), '1')


def test_shot_end_data():
    eq_(djitemdata.shot_end_data(shot, dr), '50')


class Test_ShotItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.ShotItemData(shot)

    def test_column_count(self):
        eq_(self.idata.column_count(), 5)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "Shot01")
        eq_(self.idata.data(1, dr), "closeup of plant")
        eq_(self.idata.data(2, dr), "50")
        eq_(self.idata.data(3, dr), "1")
        eq_(self.idata.data(4, dr), "50")


def test_task_name_data():
    eq_(djitemdata.task_name_data(task, dr), 'Design')


def test_task_short_data():
    eq_(djitemdata.task_short_data(task, dr), 'des')


class Test_TaskItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.TaskItemData(task)

    def test_column_count(self):
        eq_(self.idata.column_count(), 2)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "Design")
        eq_(self.idata.data(1, dr), "des")


def test_taskfile_path_data():
    eq_(djitemdata.taskfile_path_data(tfile, dr), 'anicepath')
    eq_(djitemdata.taskfile_path_data(tfile, er), 'anicepath')


def test_taskfile_version_data():
    eq_(djitemdata.taskfile_version_data(tfile, dr), 'v005')


def test_taskfile_user_data():
    eq_(djitemdata.taskfile_user_data(tfile, dr), 'Uz')
    eq_(djitemdata.taskfile_user_data(tfile, er), 'Uz')


def test_taskfile_created_data():
    now = datetime.now()
    tfile.date_created = now
    eq_(djitemdata.taskfile_created_data(tfile, dr), dt_to_qdatetime(now))
    eq_(djitemdata.taskfile_created_data(tfile, er), dt_to_qdatetime(now))


def test_taskfile_updated_data():
    now = datetime.now()
    tfile.date_updated = now
    eq_(djitemdata.taskfile_updated_data(tfile, dr), dt_to_qdatetime(now))
    eq_(djitemdata.taskfile_updated_data(tfile, er), dt_to_qdatetime(now))


def test_taskfile_rtype_data():
    eq_(djitemdata.taskfile_rtype_data(tfile, dr), 'handoff')


class Test_TaskFileItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.TaskFileItemData(tfile)

    def test_column_count(self):
        eq_(self.idata.column_count(), 6)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "v005")
        eq_(self.idata.data(1, dr), "handoff")
        eq_(self.idata.data(2, dr), "anicepath")
        eq_(self.idata.data(3, dr), "Uz")
        eq_(self.idata.data(2, er), "anicepath")
        eq_(self.idata.data(3, er), "Uz")


def test_atype_name_data():
    eq_(djitemdata.atype_name_data(atype, dr), "matte")


def test_atype_description_data():
    eq_(djitemdata.atype_description_data(atype, dr), "matte paintings")


class Test_AtypeItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.AtypeItemData(atype)

    def test_column_count(self):
        eq_(self.idata.column_count(), 2)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "matte")
        eq_(self.idata.data(1, dr), "matte paintings")


def test_asset_name_data():
    eq_(djitemdata.asset_name_data(asset, dr), "piranha plant")


def test_asset_description_data():
    eq_(djitemdata.asset_description_data(asset, dr), "eats mario")


class Test_AssetItemData():
    @classmethod
    def setup_class(cls):
        cls.idata = djitemdata.AssetItemData(asset)

    def test_column_count(self):
        eq_(self.idata.column_count(), 2)

    def test_column_data(self):
        eq_(self.idata.data(0, dr), "piranha plant")
        eq_(self.idata.data(1, dr), "eats mario")
