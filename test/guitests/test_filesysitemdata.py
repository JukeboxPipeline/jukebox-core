import pytest
from PySide import QtCore

from jukeboxcore.gui import filesysitemdata as fsitd
from jukeboxcore.filesys import JB_File


dr = QtCore.Qt.DisplayRole


def test_tfi_element_data(taskfileinfo):
    assert fsitd.taskfile_element_data(taskfileinfo, dr) == "Shot01"


def test_tfi_task_data(taskfileinfo):
    assert fsitd.taskfile_task_data(taskfileinfo, dr) == "Design"


def test_tfi_descriptor_data(taskfileinfo):
    assert fsitd.taskfile_descriptor_data(taskfileinfo, dr) == "desc1"


def test_tfi_path_data(taskfileinfo):
    assert fsitd.taskfile_path_data(taskfileinfo, dr) == JB_File(taskfileinfo).get_fullpath()


def test_tfi_version_data(taskfileinfo):
    assert fsitd.taskfile_version_data(taskfileinfo, dr) == 5


def test_tfi_rtype_data(taskfileinfo):
    assert fsitd.taskfile_rtype_data(taskfileinfo, dr) == 'handoff'


@pytest.fixture(scope="module")
def tfidata(taskfileinfo):
    return fsitd.TaskFileInfoItemData(taskfileinfo)


def test_tfidata_column_count(tfidata):
    assert tfidata.column_count(), 6


def test_tfidata_internal_data(tfidata, taskfileinfo):
    assert tfidata.internal_data() is taskfileinfo


def test_tfidata_data(tfidata, taskfileinfo):
    assert tfidata.data(0, dr) == "Shot01"
    assert tfidata.data(1, dr) == "Design"
    assert tfidata.data(2, dr) == "desc1"
    assert tfidata.data(3, dr) == 5
    assert tfidata.data(4, dr) == "handoff"
    assert tfidata.data(5, dr) == JB_File(taskfileinfo).get_fullpath()
