import pytest
from PySide import QtCore

from jukeboxcore.gui import filesysitemdata as fsitd
from jukeboxcore.filesys import JB_File


dr = QtCore.Qt.DisplayRole


def test_tfi_element_data(taskfileinfo):
    assert fsitd.taskfileinfo_element_data(taskfileinfo, dr) == "Shot01"


def test_tfi_task_data(taskfileinfo):
    assert fsitd.taskfileinfo_task_data(taskfileinfo, dr) == "Design"


def test_tfi_descriptor_data(taskfileinfo):
    assert fsitd.taskfileinfo_descriptor_data(taskfileinfo, dr) == "desc1"


def test_tfi_path_data(taskfileinfo):
    assert fsitd.taskfileinfo_path_data(taskfileinfo, dr) == JB_File(taskfileinfo).get_fullpath()


def test_tfi_version_data(taskfileinfo):
    assert fsitd.taskfileinfo_version_data(taskfileinfo, dr) == "v005"


def test_tfi_rtype_data(taskfileinfo):
    assert fsitd.taskfileinfo_rtype_data(taskfileinfo, dr) == 'handoff'


@pytest.fixture(scope="module")
def tfidata(taskfileinfo):
    return fsitd.TaskFileInfoItemData(taskfileinfo)


def test_tfidata_column_count(tfidata):
    assert tfidata.column_count(), 6


def test_tfidata_internal_data(tfidata, taskfileinfo):
    assert tfidata.internal_data() is taskfileinfo


@pytest.mark.parametrize("inp,expected", [(0, "Shot01"),
                                            (1, "Design"),
                                            (2, "desc1"),
                                            (3, "v005"),
                                            (4, "handoff")])
def test_tfidata_data(inp, expected, tfidata):
    assert tfidata.data(inp, dr) == expected


def test_tfidata_data_path(tfidata, taskfileinfo):
    assert tfidata.data(5, dr) == JB_File(taskfileinfo).get_fullpath()
