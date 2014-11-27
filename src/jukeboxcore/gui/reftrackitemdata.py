"""This module holds :class:`jukeboxcore.gui.treemodel.ItemData` subclasses that represent reftrack data,
e.g. a :class:`jukeboxcore.reftrack.Reftrack` object.
"""
from PySide import QtCore

from jukeboxcore import djadapter
from jukeboxcore.gui import filesysitemdata
from jukeboxcore.gui.treemodel import ItemData


def reftrack_elementgrp_data(rt, role):
    """Return the data for the elementgrp (e.g. the Assettype or Sequence)

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the elementgrp
    :rtype: depending on role
    :raises: TypeError
    """
    element = rt.get_element()
    if isinstance(element, djadapter.models.Shot):
        egrp = element.sequence
    elif isinstance(element, djadapter.models.Asset):
        egrp = element.atype
    else:
        raise TypeError("Expected the element to be either Asset or Shot. Got %s" % type(element))

    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return egrp.name


def reftrack_element_data(rt, role):
    """Return the data for the element (e.g. the Asset or Shot)

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the element
    :rtype: depending on role
    :raises: None
    """
    element = rt.get_element()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return element.name


def reftrack_task_data(rt, role):
    """Return the data for the task that is loaded by the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the task
    :rtype: depending on role
    :raises: None
    """
    tfi = rt.get_taskfileinfo()
    if not tfi:
        return
    return filesysitemdata.taskfileinfo_task_data(tfi, role)


def reftrack_rtype_data(rt, role):
    """Return the data for the releasetype that is loaded by the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the releasetype
    :rtype: depending on role
    :raises: None
    """
    tfi = rt.get_taskfileinfo()
    if not tfi:
        return
    return filesysitemdata.taskfileinfo_rtype_data(tfi, role)


def reftrack_descriptor_data(rt, role):
    """Return the data for the descriptor that is loaded by the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the descriptor
    :rtype: depending on role
    :raises: None
    """
    tfi = rt.get_taskfileinfo()
    if not tfi:
        return
    return filesysitemdata.taskfileinfo_descriptor_data(tfi, role)


def reftrack_version_data(rt, role):
    """Return the data for the version that is loaded by the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the version
    :rtype: depending on role
    :raises: None
    """
    tfi = rt.get_taskfileinfo()
    if not tfi:
        return
    return filesysitemdata.taskfileinfo_version_data(tfi, role)


def reftrack_status_data(rt, role):
    """Return the data for the status

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the status
    :rtype: depending on role
    :raises: None
    """
    status = rt.status()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        if status:
            return status
        else:
            return "Not in scene!"


def reftrack_uptodate_data(rt, role):
    """Return the data for the uptodate status

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the uptodate status
    :rtype: depending on role
    :raises: None
    """
    uptodate = rt.uptodate()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        if uptodate:
            return "Yes"
        else:
            return "No"


def reftrack_alien_data(rt, role):
    """Return the data for the alien status

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the alien status
    :rtype: depending on role
    :raises: None
    """
    alien = rt.alien()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        if alien:
            return "Yes"
        else:
            return "No"


def reftrack_path_data(rt, role):
    """Return the data for the path that is loaded by the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the path
    :rtype: depending on role
    :raises: None
    """
    tfi = rt.get_taskfileinfo()
    if not tfi:
        return
    return filesysitemdata.taskfileinfo_path_data(tfi, role)


class ReftrackItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a :class:`jukeboxcore.reftrack.Reftrack`
    """

    def __init__(self, reftrack):
        """Constructs a new item data for the reftrack

        :param reftrack: the reftrack to represent
        :type reftrack: :class:`jukeboxcore.reftrack.Reftrack`
        :raises: None
        """
        super(ReftrackItemData, self).__init__()
        self._reftrack = reftrack

    columns = [reftrack_elementgrp_data,
               reftrack_element_data,
               reftrack_task_data,
               reftrack_rtype_data,
               reftrack_descriptor_data,
               reftrack_version_data,
               reftrack_status_data,
               reftrack_uptodate_data,
               reftrack_alien_data,
               reftrack_path_data,]

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
        return self.columns[column](self._reftrack, role)

    def internal_data(self, ):
        """Return the taskfile

        :returns: the taskfile
        :rtype: :class:`jukeboxcore.djadapter.models.TaskFile`
        :raises: None
        """
        return self._reftrack
