from datetime import datetime

import pytest
from nose.tools import eq_
from PySide import QtCore

from jukeboxcore.gui import djitemdata
from jukeboxcore.gui.main import dt_to_qdatetime

dr = QtCore.Qt.DisplayRole
er = QtCore.Qt.EditRole


def test_prj_name_data(prj):
    eq_(djitemdata.prj_name_data(prj, dr), "Pixars Plants")


def test_prj_short_data(prj):
    eq_(djitemdata.prj_short_data(prj, dr), "plants")


def test_prj_path_data(prj, prjpath):
    eq_(djitemdata.prj_path_data(prj, dr), prjpath)


def test_prj_created_data(prj):
    now = datetime.now()
    prj.date_created = now
    eq_(djitemdata.prj_created_data(prj, dr), now.isoformat(" "))


def test_prj_semester_data(prj):
    eq_(djitemdata.prj_semester_data(prj, dr), "SS14")


def test_prj_fps_data(prj):
    eq_(djitemdata.prj_fps_data(prj, dr), "25")


def test_prj_resolution_data(prj):
    eq_(djitemdata.prj_resolution_data(prj, dr), "1920 x 1080")


def test_prj_scale_data(prj):
    eq_(djitemdata.prj_scale_data(prj, dr), "cm")


def test_prj_status_data(prj):
    eq_(djitemdata.prj_status_data(prj, dr), "New")


@pytest.fixture(scope="module")
def prjdata(prj):
    return djitemdata.ProjectItemData(prj)


@pytest.fixture(scope="module")
def seqdata(seq):
    return djitemdata.SequenceItemData(seq)


@pytest.fixture(scope="module")
def shotdata(shot):
    return djitemdata.ShotItemData(shot)


@pytest.fixture(scope="module")
def taskdata(task1):
    return djitemdata.TaskItemData(task1)


@pytest.fixture(scope="module")
def taskfiledata(tfile):
    return djitemdata.TaskFileItemData(tfile)


@pytest.fixture(scope="module")
def assetdata(asset):
    return djitemdata.AssetItemData(asset)


@pytest.fixture(scope="module")
def atypedata(atype):
    return djitemdata.AtypeItemData(atype)


def test_prj_column_count(prjdata):
    eq_(prjdata.column_count(), 9)


def test_prj_column_data(prjdata):
    eq_(prjdata.data(0, dr), "Pixars Plants")
    eq_(prjdata.data(1, dr), "plants")


def test_seq_name_data(seqdata, seq):
    eq_(djitemdata.seq_name_data(seq, dr), "Seq01")


def test_seq_description_data(seqdata, seq):
    eq_(djitemdata.seq_description_data(seq, dr), "plants everywhere")


def test_seq_column_count(seqdata):
    eq_(seqdata.column_count(), 2)


def test_seq_column_data(seqdata):
    eq_(seqdata.data(0, dr), "Seq01")
    eq_(seqdata.data(1, dr), "plants everywhere")


def test_shot_name_data(shot):
    eq_(djitemdata.shot_name_data(shot, dr), 'Shot01')


def test_shot_description_data(shot):
    eq_(djitemdata.shot_description_data(shot, dr), 'closeup of plant')


def test_shot_duration_data(shot):
    eq_(djitemdata.shot_duration_data(shot, dr), '50')


def test_shot_start_data(shot):
    eq_(djitemdata.shot_start_data(shot, dr), '1001')


def test_shot_end_data(shot):
    eq_(djitemdata.shot_end_data(shot, dr), '1050')


def test_shot_column_count(shotdata):
    eq_(shotdata.column_count(), 5)


def test_shot_column_data(shotdata):
        eq_(shotdata.data(0, dr), "Shot01")
        eq_(shotdata.data(1, dr), "closeup of plant")
        eq_(shotdata.data(2, dr), "50")
        eq_(shotdata.data(3, dr), "1001")
        eq_(shotdata.data(4, dr), "1050")


def test_task_name_data(task1):
    eq_(djitemdata.task_name_data(task1, dr), 'Design')


def test_task_short_data(task1):
    eq_(djitemdata.task_short_data(task1, dr), 'des')


def test_column_count(taskdata):
    eq_(taskdata.column_count(), 2)


def test_column_data(taskdata):
    eq_(taskdata.data(0, dr), "Design")
    eq_(taskdata.data(1, dr), "des")


def test_taskfile_path_data(tfile):
    eq_(djitemdata.taskfile_path_data(tfile, dr), 'anicepath')
    eq_(djitemdata.taskfile_path_data(tfile, er), 'anicepath')


def test_taskfile_version_data(tfile):
    eq_(djitemdata.taskfile_version_data(tfile, dr), 'v005')


def test_taskfile_user_data(tfile, user):
    eq_(djitemdata.taskfile_user_data(tfile, dr), user.username)
    eq_(djitemdata.taskfile_user_data(tfile, er), user.username)


def test_taskfile_created_data(tfile):
    now = datetime.now()
    tfile.date_created = now
    eq_(djitemdata.taskfile_created_data(tfile, dr), dt_to_qdatetime(now))
    eq_(djitemdata.taskfile_created_data(tfile, er), dt_to_qdatetime(now))


def test_taskfile_updated_data(tfile):
    now = datetime.now()
    tfile.date_updated = now
    eq_(djitemdata.taskfile_updated_data(tfile, dr), dt_to_qdatetime(now))
    eq_(djitemdata.taskfile_updated_data(tfile, er), dt_to_qdatetime(now))


def test_taskfile_rtype_data(tfile):
    eq_(djitemdata.taskfile_rtype_data(tfile, dr), 'handoff')


def test_taskfile_column_count(taskfiledata):
    eq_(taskfiledata.column_count(), 6)


def test_taskfile_column_data(taskfiledata, user):
    eq_(taskfiledata.data(0, dr), "v005")
    eq_(taskfiledata.data(1, dr), "handoff")
    eq_(taskfiledata.data(2, dr), "anicepath")
    eq_(taskfiledata.data(3, dr), user.username)
    eq_(taskfiledata.data(2, er), "anicepath")
    eq_(taskfiledata.data(3, er), user.username)


def test_atype_name_data(atype):
    eq_(djitemdata.atype_name_data(atype, dr), "matte")


def test_atype_description_data(atype):
    eq_(djitemdata.atype_description_data(atype, dr), "matte paintings")


def test_assettype_column_count(atypedata):
    eq_(atypedata.column_count(), 2)


def test_assettype_column_data(atypedata):
    eq_(atypedata.data(0, dr), "matte")
    eq_(atypedata.data(1, dr), "matte paintings")


def test_asset_name_data(asset):
    eq_(djitemdata.asset_name_data(asset, dr), "piranha plant")


def test_asset_description_data(asset):
    eq_(djitemdata.asset_description_data(asset, dr), "eats mario")


def test_asset_column_count(assetdata):
    eq_(assetdata.column_count(), 2)


def test_asset_column_data(assetdata):
    eq_(assetdata.data(0, dr), "piranha plant")
    eq_(assetdata.data(1, dr), "eats mario")
