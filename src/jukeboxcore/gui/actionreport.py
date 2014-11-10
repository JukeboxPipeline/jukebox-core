"""This module provides a way to display the result of an :class:`jukeboxcore.action.ActionCollection` to the user."""
from PySide import QtCore, QtGui

from jukeboxcore.gui.treemodel import TreeModel, ItemData, ListItemData, TreeItem
from jukeboxcore.action import ActionStatus


class ActionItemData(ItemData):
    """A class that holds data of a :class:`jukeboxcore.action.ActionUnit`
    """

    colormapping = {ActionStatus.SUCCESS: QtGui.QColor(QtCore.Qt.green),
                    ActionStatus.FAILURE: QtGui.QColor(255, 153, 51),
                    ActionStatus.ERROR: QtGui.QColor(QtCore.Qt.red),
                    ActionStatus.SKIPPED: QtGui.QColor(QtCore.Qt.yellow)}

    def __init__(self, actionunit):
        """Create a new ActionItemData for the given actionunit

        :param actionunit: a action unit
        :type actionunit: :class:`jukeboxcore.action.ActionUnit`
        :raises: None
        """
        super(ActionItemData, self).__init__()
        self._au = actionunit

    def data(self, column, role):
        """Return the data for the specified column and role

        Column 0: The name of the action
        Column 1: The description of the action
        Column 2: The status value
        Column 3: The status message
        Column 4: The traceback

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role, or None if the column is out of range
        :rtype: depending on the role or None
        :raises: None
        """
        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return self._au.name
            if column == 1:
                return self._au.description
            if column == 2:
                return self._au.status.value
            if column == 3:
                return self._au.status.message
            if column == 4:
                return self._au.status.traceback

        if role == QtCore.Qt.ForegroundRole:
            if column == 2:
                return self.colormapping.get(self._au.status.value)

    def column_count(self, ):
        """Return the number of columns, 5

        :returns: 5
        :rtype: int
        :raises: None
        """
        return 5

    def internal_data(self, ):
        """Return the action unit

        :returns: the action unit
        :rtype: :class:`jukeboxcore.action.ActionUnit`
        :raises: None
        """
        return self._au

    def flags(self, column):
        """Return the item flags for the item

        Default is QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        Column 4 is also editable.

        :param column: the column to query
        :type column: int
        :returns: the item flags.
        :rtype: QtCore.Qt.ItemFlags
        :raises: None
        """
        flags = super(ActionItemData, self).flags(column)
        if (column == 3 and self._au.status.message) or (column == 4 and self._au.status.traceback):
            flags = flags | QtCore.Qt.ItemIsEditable
        return flags


def create_action_model(actioncollection):
    """Create and return a new model for the given actioncollection

    :param actioncollection: the action collection that should get a model
    :type actioncollection: :class:`jukeboxcore.action.ActionCollection`
    :returns: the created model
    :rtype: :class:`TreeModel`
    :raises: None
    """
    rootdata = ListItemData(["Name", "Description", "Status", "Message", "Traceback"])
    root = TreeItem(rootdata)
    for au in actioncollection.actions:
        adata = ActionItemData(au)
        TreeItem(adata, parent=root)
    return TreeModel(root)
