"""This module provides a generic interface for tree models

It centers around the TreeModel, which is used for all kinds of trees.
The tree gets customized by the TreeItems. Each TreeItem holds
a specific ItemData subclass. The ItemData is responsible for
delivering the data. Make sure that all TreeItems in one hierarchy have the same ItemData subclasses or at least the same column_count.
If not, make sure the data method can handle columns outside their column count.
If you want to create a tree, create the needed itemdata classes,
create a root tree item that is parent for all top-level items.
The root item does not have to provide data, so the data might be None.
It is advides to use :class:`jukeboxcore.gui.treemodel.ListItemData` because the data in the list
will be used for the headers.
Then create the tree items with their appropriate data instances.
Finally create a tree model instance with the root tree item.
"""

import abc

from PySide import QtCore


class ItemData(object):  # pragma: no cover
    """An abstract class that holds data and is used as an interface for TreeItems

    When subclassing implement :meth:`ItemData.data` and :meth:`ItemData.column_count`.
    It is advised to reimplement :meth:`ItemData.internal_data` too.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.
        When used in a root item, the data should return the horizontal header
        data. When returning None, the section Number is used (starting at 1) by the treemodel.
        So if you want an empty header, return an empty string!

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        pass

    @abc.abstractmethod
    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        pass

    def internal_data(self, ):
        """Return the internal data of the ItemData

        E.g. a ListItemData could return the list it uses, a
        ProjectItemData could return the Project etc.

        :returns: the data the itemdata uses as information
        :rtype: None|arbitrary data
        :raises: None
        """
        return None

    def flags(self, column):
        """Return the item flags for the item

        Default is QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        :param column: the column to query
        :type column: int
        :returns: the item flags
        :rtype: QtCore.Qt.ItemFlags
        :raises: None
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class ListItemData(ItemData):
    """Item data for generic lists

    Initialize it with a list of objects. Each element corresponds to a column.
    For DisplayRole the objects are converted to strings with ``str()``.
    """

    def __init__(self, liste):
        """ Constructs a new StringItemData with the given list

        :param list: a list of objects, one for each column
        :type list: list of objects
        :raises: None
        """
        super(ListItemData, self).__init__()
        self._list = liste

    def data(self, column, role):
        """Return the data for the specified column and role

        For DisplayRole the element in the list will be converted to a sting and returned.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role, or None if the column is out of range
        :rtype: depending on the role or None
        :raises: None
        """
        if role == QtCore.Qt.DisplayRole:
            if column >= 0 and column < len(self._list):
                return str(self._list[column])

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self._list)

    def internal_data(self, ):
        """Return the list

        :returns: the internal list
        :rtype: :class:`list`
        :raises: None
        """
        return self._list


class TreeItem(object):
    """General TreeItem

    You can represent a tree structure with these tree items. Each item
    should contain some data that it can give to the model.
    Note that each tree always has one root item.
    Even if you have multiple top level items, they are all grouped under one
    root. The data for the root item can be None but it is advised to use
    a ListItemData so you can provide horizontal headers.

    TreeItems should always belong to only one model.
    Once a new TreeModel gets initialized all TreeItems will share the same model.
    When you add a new Item or delete one, the model gets automatically updated.
    You do not need to call TreeModel insertRow or removeRow. Just use add_child, remove_child
    or create a new TreeItem and provide a parent item to the constructor.
    """

    def __init__(self, data, parent=None):
        """Constructs a new TreeItem that holds some data and might be parented under parent

        :param data: the data item. if the tree item is the root, the data will be used for horizontal headers!
                     It is recommended to use :class:`jukeboxcore.gui.treeitem.ListItemData` in that case.
        :type data: :class:`jukeboxcore.gui.treemodel.ItemData`
        :param parent: the parent treeitem
        :type parent: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :raises: None
        """
        self._model = None
        self._data = data
        self._parent = parent
        self.childItems = []
        if self._parent is not None:
            self._parent.add_child(self)

    def get_model(self, ):
        """Return the model the item belongs to

        :returns: the model the item belongs to or None if it belongs to none
        :rtype: :class:`TreeModel` | None
        :raises: None
        """
        return self._model

    def set_model(self, model):
        """Set the model the item belongs to

        A TreeItem can only belong to one model.

        :param model: the model the item belongs to
        :type model: :class:`Treemodel`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._model = model
        for c in self.childItems:
            c.set_model(model)

    def add_child(self, child):
        """Add child to children of this TreeItem

        :param child: the child TreeItem
        :type child: :class:`TreeItem`
        :returns: None
        :rtype: None
        :raises: None
        """
        child.set_model(self._model)
        if self._model:
            row = len(self.childItems)
            parentindex = self._model.index_of_item(self)
            self._model.insertRow(row, child, parentindex)
        else:
            self.childItems.append(child)

    def remove_child(self, child):
        """Remove the child from this TreeItem

        :param child: the child TreeItem
        :type child: :class:`TreeItem`
        :returns: None
        :rtype: None
        :raises: ValueError
        """
        child.set_model(None)
        if self._model:
            row = self.childItems.index(child)
            parentindex = self._model.index_of_item(self)
            self._model.removeRow(row, parentindex)
        else:
            self.childItems.remove(child)

    def child(self, row):
        """Return the child at the specified row

        :param row: the row number
        :type row: int
        :returns: the child
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :raises: IndexError
        """
        return self.childItems[row]

    def child_count(self, ):
        """Return the number of children

        :returns: child coun
        :rtype: int
        :raises: None
        """
        return len(self.childItems)

    def row(self, ):
        """Return the index of this tree item in the parent rows

        :returns: the row of this TreeItem in the parent
        :rtype: int
        :raises: None
        """
        if self._parent is None:
            return 0
        return self._parent.childItems.index(self)

    def column_count(self, ):
        """Return the number of columns that the children have

        If there are no children, return the column count of its own data.

        :returns: the column count of the children data
        :rtype: int
        :raises: None
        """
        if self.child_count():
            return self.childItems[0]._data.column_count()
        else:
            return self._data.column_count() if self._data else 0

    def data(self, column, role):
        """Return the data for the column and role

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        if self._data is not None and (column >= 0 or column < self._data.column_count()):
            return self._data.data(column, role)

    def parent(self, ):
        """Return the parent tree item

        :returns: the parent or None if there is no parent
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :raises: None
        """
        return self._parent

    def set_parent(self, parent):
        """Set the parent of the treeitem

        :param parent: parent treeitem
        :type parent: :class:`TreeItem` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._parent == parent:
            return
        if self._parent:
            self._parent.remove_child(self)
        self._parent = parent
        if parent:
            parent.add_child(self)

    def itemdata(self, ):
        """Return the internal :class:`ItemData`

        :returns: the internal ItemData
        :rtype: :class:`ItemData`
        :raises: None
        """
        return self._data

    def internal_data(self, ):
        """Return the internal data of the item data

        E.g. a ListItemData could return the list it uses, a
        ProjectItemData could return the Project etc.

        :returns: the data the itemdata uses as information
        :rtype: None|arbitrary data
        :raises: None
        """
        return self._data.internal_data()

    def flags(self, index):
        """Return the flags for the item

        :param index: the index to query
        :type index: :class:`QtCore.QModelIndex`
        :returns: the flags
        :rtype: QtCore.Qt.ItemFlags
        :raises: None
        """
        return self._data.flags(index.column())


class TreeModel(QtCore.QAbstractItemModel):
    """A tree model that uses the :class:`jukeboxcore.gui.treemodel.TreeItem` to represent a general tree.

    """

    def __init__(self, root, parent=None):
        """Constructs a new tree model with the given root treeitem

        :param root: the root tree item. The root tree item is responsible for the headers.
                     A :class:`ListItemData` with the headers is suitable as data for the item.
        :type root: :class:`TreeItem`
        :param parent: the parent for the model
        :type parent: :class:`QtCore.QObject`
        :raises: None
        """
        super(TreeModel, self).__init__(parent)
        self._root = root
        self._root.set_model(self)

    def index(self, row, column, parent=None):
        """Returns the index of the item in the model specified by the given row, column and parent index.

        :param row: the row of the item
        :type row: int
        :param column: the column for the item
        :type column: int
        :param parent: the parent index
        :type parent: :class:`QtCore.QModelIndex`:
        :returns: the index of the item
        :rtype: :class:`QtCore.QModelIndex`
        :raises: None
        """
        if parent is None:
            parent = QtCore.QModelIndex()
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self._root

        try:
            childItem = parentItem.child(row)
            return self.createIndex(row, column, childItem)
        except IndexError:
            return QtCore.QModelIndex()

    def parent(self, index):
        """Returns the parent of the model item with the given index. If the item has no parent, an invalid QModelIndex is returned.

        :param index: the index that you want to know the parent of
        :type index: :class:`QtCore.QModelIndex`
        :returns: parent index
        :rtype: :class:`QtCore.QModelIndex`
        :raises: None
        """
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem is self._root:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        """Returns the number of rows under the given parent.
        When the parent is valid it means that rowCount is returning the number
        of children of parent.

        :param parent: the parent index
        :type parent: :class:`QtCore.QModelIndex`:
        :returns: the row count
        :rtype: int
        :raises: None
        """
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()
        return parentItem.child_count()

    def columnCount(self, parent):
        """Returns the number of columns for the children of the given parent.

        :param parent: the parent index
        :type parent: :class:`QtCore.QModelIndex`:
        :returns: the column count
        :rtype: int
        :raises: None
        """
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self._root.column_count()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Returns the data stored under the given role for the item referred to by the index.

        :param index: the index
        :type index: QModelIndex
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: some data depending on the role
        :raises: None
        """
        if not index.isValid():
            return
        item = index.internalPointer()
        return item.data(index.column(), role)

    def headerData(self, section, orientation, role):
        """

        :param section:
        :type section:
        :param orientation:
        :type orientation:
        :param role:
        :type role:
        :returns: None
        :rtype: None
        :raises: None
        """
        if orientation == QtCore.Qt.Horizontal:
            d = self._root.data(section, role)
            if d is None and role == QtCore.Qt.DisplayRole:
                return str(section+1)
            return d
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return str(section+1)

    def insertRow(self, row, item, parent):
        """Inserts a single item before the given row in the child items of the parent specified.

        :param row: the index where the rows get inserted
        :type row: int
        :param item: the item to insert. When creating the item, make sure it's parent is None.
                     If not it will defeat the purpose of this function.
        :type item: :class:`TreeItem`
        :param parent: the parent
        :type parent: :class:`QtCore.QModelIndex`
        :returns: Returns true if the row is inserted; otherwise returns false.
        :rtype: bool
        :raises: None
        """
        item.set_model(self)
        if parent.isValid():
            parentitem = parent.internalPointer()
        else:
            parentitem = self._root
        self.beginInsertRows(parent, row, row)
        item._parent = parentitem
        if parentitem:
            parentitem.childItems.insert(row, item)
        self.endInsertRows()
        return True

    def removeRow(self, row, parent):
        """Remove row from parent

        :param row: the row index
        :type row: int
        :param parent: the parent index
        :type parent: :class:`QtCore.QModelIndex`
        :returns: True if row is inserted; otherwise returns false.
        :rtype: bool
        :raises: None
        """
        if parent.isValid():
            parentitem = parent.internalPointer()
        else:
            parentitem = self._root
        self.beginRemoveRows(parent, row, row)
        item = parentitem.childItems[row]
        item.set_model(None)
        item._parent = None
        del parentitem.childItems[row]
        self.endRemoveRows()
        return True

    @property
    def root(self, ):
        """Return the root tree item

        :returns: the root item
        :rtype: :class:`TreeItem`
        :raises: None
        """
        return self._root

    def flags(self, index):
        """

        :param index: the index to query
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        if index.isValid():
            item = index.internalPointer()
            return item.flags(index)
        else:
            super(TreeModel, self).flags(index)

    def index_of_item(self, item):
        """Get the index for the given TreeItem

        :param item: the treeitem to query
        :type item: :class:`TreeItem`
        :returns: the index of the item
        :rtype: :class:`QtCore.QModelIndex`
        :raises: ValueError
        """
        # root has an invalid index
        if item == self._root:
            return QtCore.QModelIndex()
        # find all parents to get their index
        parents = [item]
        i = item
        while True:
            parent = i.parent()
            # break if parent is root because we got all parents we need
            if parent == self._root:
                break
            if parent is None:
                # No new parent but last parent wasn't root!
                # This means that the item was not in the model!
                return QtCore.QModelIndex()
            # a new parent was found and we are still not at root
            # search further until we get to root
            i = parent
            parents.append(parent)

        # get the parent indexes until
        index = QtCore.QModelIndex()
        for treeitem in reversed(parents):
            parent = treeitem.parent()
            row = parent.childItems.index(treeitem)
            index = self.index(row, 0, index)
        return index
