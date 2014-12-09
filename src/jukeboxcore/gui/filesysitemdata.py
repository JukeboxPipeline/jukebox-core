"""This module holds :class:`jukeboxcore.gui.treemodel.ItemData` subclasses that represent filesys data,
e.g. a :class:`jukeboxcore.filesys.TaskFileInfo`
"""
from PySide import QtCore

from jukeboxcore.gui.treemodel import ItemData
from jukeboxcore.filesys import JB_File


def taskfileinfo_element_data(tfi, role):
    """Return the data for the element (e.g. the Asset or Shot)

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the element
    :rtype: depending on role
    :raises: None
    """
    task = tfi.task
    element = task.element
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return element.name


def taskfileinfo_task_data(tfi, role):
    """Return the data for task

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the task
    :rtype: depending on role
    :raises: None
    """
    task = tfi.task
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return task.name


def taskfileinfo_descriptor_data(tfi, role):
    """Return the data for descriptor

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the descriptor
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return tfi.descriptor


def taskfileinfo_path_data(tfi, role):
    """Return the data for path

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the path
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return JB_File(tfi).get_fullpath()


def taskfileinfo_version_data(tfi, role):
    """Return the data for version

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` that holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the version
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return 'v%03i' % tfi.version


def taskfileinfo_rtype_data(tfi, role):
    """Return the data for rtype

    :param tfi: the :class:`jukeboxcore.filesys.TaskFileInfo` that holds the data
    :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the releasetype
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return tfi.releasetype


class TaskFileInfoItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a :class:`jukeboxcore.filesys.TaskFileInfo`
    """

    def __init__(self, taskfileinfo):
        """Constructs a new item data for the taskfileinfo

        :param taskfileinfo: the taskfileinfo to represent
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :raises: None
        """
        super(TaskFileInfoItemData, self).__init__()
        self._taskfileinfo = taskfileinfo

    columns = [taskfileinfo_element_data,
               taskfileinfo_task_data,
               taskfileinfo_descriptor_data,
               taskfileinfo_version_data,
               taskfileinfo_rtype_data,
               taskfileinfo_path_data,]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._taskfileinfo, role)

    def internal_data(self, ):
        """Return the taskfileinfo

        :returns: the taskfileinfo
        :rtype: :class:`jukeboxcore.filesys.TaskFileInfo`
        :raises: None
        """
        return self._taskfileinfo
