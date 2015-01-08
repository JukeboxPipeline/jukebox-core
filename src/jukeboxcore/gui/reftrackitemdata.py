"""This module holds :class:`jukeboxcore.gui.treemodel.ItemData` subclasses that represent reftrack data,
e.g. a :class:`jukeboxcore.reftrack.Reftrack` object.
"""
from functools import partial

from PySide import QtCore, QtGui

from jukeboxcore import djadapter
from jukeboxcore.gui import filesysitemdata
from jukeboxcore.gui.treemodel import ItemData


UPTODATE_RGB = (53, 69, 41)
"""RGB values for the color, when a reftrack is uptodate"""
OUTDATED_RGB = (69, 41, 41)
"""RGB values for the color, when a reftrack is outdated"""


REFTRACK_OBJECT_ROLE = QtCore.Qt.UserRole + 1


def reftrack_type_data(rt, role):
    """Return the data for the type (e.g. Asset, Alembic, Camera etc)

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the type
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return rt.get_typ()
    elif role == QtCore.Qt.DecorationRole:
        return rt.get_typ_icon()


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
    elif element is not None:
        raise TypeError("Expected the element to be either Asset or Shot. Got %s" % type(element))
    else:
        return
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
    if element is None:
        return
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
    if role == QtCore.Qt.ForegroundRole:
        if uptodate:
            return QtGui.QColor(*UPTODATE_RGB)
        elif rt.status():
            return QtGui.QColor(*OUTDATED_RGB)


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


def reftrack_restricted_data(rt, role, attr):
    """Return the data for restriction of the given attr of the given reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the restriction
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        if rt.is_restricted(getattr(rt, attr, None)):
            return "Restricted"
        else:
            return "Allowed"


def reftrack_id_data(rt, role):
    """Return the data for the id of the reftrack

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the id
    :rtype: depending on the role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return rt.get_id()


def reftrack_object_data(rt, role):
    """Return the reftrack for REFTRACK_OBJECT_ROLE

    :param rt: the :class:`jukeboxcore.reftrack.Reftrack` holds the data
    :type rt: :class:`jukeboxcore.reftrack.Reftrack`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the id
    :rtype: depending on the role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return str(rt)
    if role == REFTRACK_OBJECT_ROLE:
        return rt


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

    columns = [reftrack_type_data,
               reftrack_elementgrp_data,
               reftrack_element_data,
               reftrack_task_data,
               reftrack_rtype_data,
               reftrack_descriptor_data,
               reftrack_version_data,
               reftrack_status_data,
               reftrack_uptodate_data,
               reftrack_alien_data,
               reftrack_path_data,
               partial(reftrack_restricted_data, attr='reference'),
               partial(reftrack_restricted_data, attr='load'),
               partial(reftrack_restricted_data, attr='unload'),
               partial(reftrack_restricted_data, attr='import_reference'),
               partial(reftrack_restricted_data, attr='import_taskfile'),
               partial(reftrack_restricted_data, attr='replace'),
               reftrack_id_data,
               reftrack_object_data]

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

    def flags(self, column):
        """Return the item flags for the item

        Default is QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        :param column: the column to query
        :type column: int
        :returns: the item flags
        :rtype: QtCore.Qt.ItemFlags
        :raises: None
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


class ReftrackSortFilterModel(QtGui.QSortFilterProxyModel):
    """A sort filter proxy model, that can filter rows in a treemodel
    that uses ReftrackItemDatas.
    """

    def __init__(self, parent=None):
        """Initialize a new reftrack sort filter model

        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :raises: None
        """
        super(ReftrackSortFilterModel, self).__init__(parent)
        # lists of forbidden values for different attributes
        self._forbidden_status = []
        self._forbidden_types = []
        self._forbidden_uptodate = []
        self._forbidden_alien = []

    def filterAcceptsRow(self, row, parentindex):
        """Return True, if the filter accepts the given row of the parent

        :param row: the row to filter
        :type row: :class:`int`
        :param parentindex: the parent index
        :type parentindex: :class:`QtCore.QModelIndex`
        :returns: True, if the filter accepts the row
        :rtype: :class:`bool`
        :raises: None
        """
        if not super(ReftrackSortFilterModel, self).filterAcceptsRow(row, parentindex):
            return False
        if parentindex.isValid():
            m = parentindex.model()
        else:
            m = self.sourceModel()

        i = m.index(row, 18, parentindex)
        reftrack = i.data(REFTRACK_OBJECT_ROLE)
        if not reftrack:
            return True
        else:
            return self.filter_accept_reftrack(reftrack)

    def filter_accept_reftrack(self, reftrack):
        """Return True, if the filter accepts the given reftrack

        :param reftrack: the reftrack to filter
        :type reftrack: :class:`jukeboxcore.reftrack.Reftrack`
        :returns: True, if the filter accepts the reftrack
        :rtype: :class:`bool`
        :raises: None
        """
        if reftrack.status() in self._forbidden_status:
            return False
        if reftrack.get_typ() in self._forbidden_types:
            return False
        if reftrack.uptodate() in self._forbidden_uptodate:
            return False
        if reftrack.alien() in self._forbidden_alien:
            return False
        return True

    def set_forbidden_statuses(self, statuses):
        """Set all forbidden status values

        :param statuses: a list with forbidden status values
        :type statuses: list
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._forbidden_status == statuses:
            return
        self._forbidden_status = statuses
        self.invalidateFilter()

    def get_forbidden_statuses(self, ):
        """Return all forbidden status values

        :returns: a list with forbidden status values
        :rtype: list
        :raises: None
        """
        return self._forbidden_status

    def set_forbidden_types(self, types):
        """Set all forbidden type values

        :param typees: a list with forbidden type values
        :type typees: list
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._forbidden_types == types:
            return
        self._forbidden_types = types
        self.invalidateFilter()

    def get_forbidden_types(self, ):
        """Return all forbidden type values

        :returns: a list with forbidden type values
        :rtype: list
        :raises: None
        """
        return self._forbidden_types

    def set_forbidden_uptodate(self, uptodate):
        """Set all forbidden uptodate values

        :param uptodatees: a list with forbidden uptodate values
        :uptodate uptodatees: list
        :returns: None
        :ruptodate: None
        :raises: None
        """
        if self._forbidden_uptodate == uptodate:
            return
        self._forbidden_uptodate = uptodate
        self.invalidateFilter()

    def get_forbidden_uptodates(self, ):
        """Return all forbidden uptodate values

        :returns: a list with forbidden uptodate values
        :ruptodate: list
        :raises: None
        """
        return self._forbidden_uptodate

    def set_forbidden_alien(self, alien):
        """Set all forbidden alien values

        :param alienes: a list with forbidden alien values
        :alien alienes: list
        :returns: None
        :ralien: None
        :raises: None
        """
        if self._forbidden_alien == alien:
            return
        self._forbidden_alien = alien
        self.invalidateFilter()

    def get_forbidden_aliens(self, ):
        """Return all forbidden alien values

        :returns: a list with forbidden alien values
        :ralien: list
        :raises: None
        """
        return self._forbidden_alien
