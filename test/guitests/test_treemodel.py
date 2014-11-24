from nose.tools import eq_
from PySide import QtCore

from jukeboxcore.gui import treemodel

dr = QtCore.Qt.DisplayRole


class Test_ListItemData():

    @classmethod
    def setup_class(cls):
        cls.strlist = ['a', 'b', 'hallo']
        cls.intlist = [1, 2, 3, 4, 5, 6]
        cls.mixedlist = ['a', None, False, 1, [1, '2']]
        cls.slistdata = treemodel.ListItemData(cls.strlist)
        cls.ilistdata = treemodel.ListItemData(cls.intlist)
        cls.mixeddata = treemodel.ListItemData(cls.mixedlist)

    def test_column_count(self):
        eq_(self.slistdata.column_count(), 3)
        eq_(self.ilistdata.column_count(), 6)
        eq_(self.mixeddata.column_count(), 5)

    def test_data(self):
        eq_(self.slistdata.data(0, dr), 'a')
        eq_(self.slistdata.data(1, dr), 'b')
        eq_(self.slistdata.data(2, dr), 'hallo')
        eq_(self.ilistdata.data(0, dr), '1')
        eq_(self.ilistdata.data(1, dr), '2')
        eq_(self.ilistdata.data(2, dr), '3')
        eq_(self.ilistdata.data(3, dr), '4')
        eq_(self.mixeddata.data(0, dr), 'a')
        eq_(self.mixeddata.data(1, dr), 'None')
        eq_(self.mixeddata.data(2, dr), 'False')
        eq_(self.mixeddata.data(3, dr), '1')
        eq_(self.mixeddata.data(4, dr), '[1, \'2\']')
        eq_(self.slistdata.data(-1, dr), None)
        eq_(self.slistdata.data(3, dr), None)
        eq_(self.slistdata.data(99, dr), None)


# stub test data
class StubItemData1(treemodel.ItemData):
    def data(self, column, role):
        if role == QtCore.Qt.DisplayRole:
            return "Data1"

    def column_count(self):
        return 1


class StubItemData2(treemodel.ItemData):
    def data(self, column, role):
        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return "Data2"
            elif column == 1:
                return "Data3"

    def column_count(self):
        return 2


class Test_TreeItem():
    def setup(self):
        self.root = treemodel.TreeItem(None)
        self.c1 = treemodel.TreeItem(StubItemData2(), self.root)
        self.c2 = treemodel.TreeItem(StubItemData2(), self.root)
        self.c3 = treemodel.TreeItem(StubItemData1(), self.c2)

    def test_child(self):
        assert self.root.child(0) is self.c1
        assert self.root.child(1) is self.c2
        assert self.c2.child(0) is self.c3

    def test_child_count(self):
        eq_(self.root.child_count(), 2)
        eq_(self.c1.child_count(), 0)
        eq_(self.c2.child_count(), 1)

    def test_row(self):
        eq_(self.root.row(), 0)
        eq_(self.c1.row(), 0)
        eq_(self.c2.row(), 1)
        eq_(self.c3.row(), 0)

    def test_column_count(self):
        eq_(self.root.column_count(), 2)
        eq_(self.c1.column_count(), 0)
        eq_(self.c2.column_count(), 1)
        eq_(self.c3.column_count(), 0)

    def test_data(self):
        dr = QtCore.Qt.DisplayRole
        eq_(self.root.data(0, dr), None)
        eq_(self.root.data(1, dr), None)
        eq_(self.c1.data(0, dr), "Data2")
        eq_(self.c1.data(1, dr), "Data3")
        eq_(self.c2.data(0, dr), "Data2")
        eq_(self.c3.data(0, dr), "Data1")

    def test_parent(self):
        assert self.root.parent() is None
        assert self.c1.parent() is self.root
        assert self.c2.parent() is self.root
        assert self.c3.parent() is self.c2


class Test_TreeModel():

    @classmethod
    def setup_class(cls):
        cls.root = treemodel.TreeItem(None)
        cls.c1 = treemodel.TreeItem(StubItemData2(), cls.root)
        cls.c2 = treemodel.TreeItem(StubItemData2(), cls.root)
        cls.c3 = treemodel.TreeItem(StubItemData1(), cls.c2)
        cls.c4 = treemodel.TreeItem(StubItemData1(), cls.c2)
        cls.c5 = treemodel.TreeItem(StubItemData1(), cls.c4)
        cls.m = treemodel.TreeModel(cls.root)

    def test_index(self):
        c1i = self.m.index(0, 0, QtCore.QModelIndex())
        assert c1i.internalPointer() is self.c1
        assert self.m.index(0, 0).internalPointer() is self.c1
        c2i = self.m.index(1, 0, QtCore.QModelIndex())
        assert c2i.internalPointer() is self.c2
        c3i = self.m.index(0, 0, c2i)
        assert c3i.internalPointer() is self.c3
        eq_(self.m.index(-1, 0), QtCore.QModelIndex())

    def test_parent(self):
        eq_(self.m.parent(QtCore.QModelIndex()), QtCore.QModelIndex())
        c1i = self.m.index(0, 0)
        c2i = self.m.index(1, 0)
        c3i = self.m.index(0, 0, c2i)
        eq_(self.m.parent(c1i), QtCore.QModelIndex())
        eq_(self.m.parent(c2i), QtCore.QModelIndex())
        eq_(self.m.parent(c3i), c2i)

    def test_row_count(self):
        c1i = self.m.index(0, 0)
        c2i = self.m.index(1, 0)
        c3i = self.m.index(0, 0, c2i)
        eq_(self.m.rowCount(QtCore.QModelIndex()), 2)
        eq_(self.m.rowCount(c1i), 0)
        eq_(self.m.rowCount(c2i), 2)
        eq_(self.m.rowCount(c3i), 0)

    def test_column_count(self):
        c1i = self.m.index(0, 0)
        c2i = self.m.index(1, 0)
        c3i = self.m.index(0, 0, c2i)
        eq_(self.m.columnCount(QtCore.QModelIndex()), 2)
        eq_(self.m.columnCount(c1i), 0)
        eq_(self.m.columnCount(c2i), 1)
        eq_(self.m.columnCount(c3i), 0)

    def test_data(self):
        c1i = self.m.index(0, 0)
        c12i = self.m.index(0, 1)
        eq_(c12i.row(), 0)
        eq_(c12i.column(), 1)
        assert c12i.internalPointer() is self.c1
        c2i = self.m.index(1, 0)
        c22i = self.m.index(1, 1)
        c3i = self.m.index(0, 0, c2i)
        assert self.m.data(QtCore.QModelIndex(), dr) is None
        eq_(self.m.data(c1i, dr), "Data2")
        eq_(self.m.data(c12i, dr), "Data3")
        eq_(self.m.data(c2i, dr), "Data2")
        eq_(self.m.data(c22i, dr), "Data3")
        eq_(self.m.data(c3i, dr), "Data1")

    def test_headerdata(self):
        eq_(self.m.headerData(0, QtCore.Qt.Horizontal, dr), '1')
        eq_(self.m.headerData(1, QtCore.Qt.Horizontal, dr), '2')
        eq_(self.m.headerData(2, QtCore.Qt.Horizontal, dr), '3')
        eq_(self.m.headerData(0, QtCore.Qt.Vertical, dr), '1')
        eq_(self.m.headerData(1, QtCore.Qt.Vertical, dr), '2')
        eq_(self.m.headerData(2, QtCore.Qt.Vertical, dr), '3')

        rootdata = treemodel.ListItemData(['Sec1', 'Head2', 'Chap3'])
        root = treemodel.TreeItem(rootdata)
        m = treemodel.TreeModel(root)
        eq_(m.headerData(0, QtCore.Qt.Horizontal, dr), 'Sec1')
        eq_(m.headerData(1, QtCore.Qt.Horizontal, dr), 'Head2')
        eq_(m.headerData(2, QtCore.Qt.Horizontal, dr), 'Chap3')
        eq_(m.headerData(3, QtCore.Qt.Horizontal, dr), '4')
        eq_(m.headerData(99, QtCore.Qt.Horizontal, dr), '100')
        eq_(m.headerData(3, QtCore.Qt.Vertical, dr), '4')
        eq_(m.headerData(99, QtCore.Qt.Vertical, dr), '100')

    def test_insertRow(self):
        root = treemodel.TreeItem(None)
        i1 = treemodel.TreeItem(StubItemData2(), root)
        m = treemodel.TreeModel(root)
        newi1 = treemodel.TreeItem(treemodel.ListItemData(['1']))
        newi2 = treemodel.TreeItem(treemodel.ListItemData(['2']))
        newi3 = treemodel.TreeItem(treemodel.ListItemData(['3']))
        parent = m.index(0, 0)
        eq_(parent.internalPointer(), i1)
        m.insertRow(0, newi1, parent)
        eq_(m.index(0, 0, parent).internalPointer(), newi1)
        m.insertRow(0, newi2, parent)
        eq_(m.index(0, 0, parent).internalPointer(), newi2)
        eq_(m.index(1, 0, parent).internalPointer(), newi1)
        m.insertRow(2, newi3, parent)
        eq_(m.index(0, 0, parent).internalPointer(), newi2)
        eq_(m.index(1, 0, parent).internalPointer(), newi1)
        eq_(m.index(2, 0, parent).internalPointer(), newi3)

    def test_index_of_item(self, ):
        assert self.root
        i1 = self.m.index_of_item(self.root)
        assert i1.row() == -1
        assert i1.column() == -1
        assert not i1.isValid()
        assert not i1.parent().isValid()
        i2 = self.m.index_of_item(self.c1)
        assert i2.row() == 0
        assert i2.column() == 0
        assert i2.parent() == i1
        i3 = self.m.index_of_item(self.c2)
        assert i3.row() == 1
        assert i3.column() == 0
        assert i3.parent() == i1
        i4 = self.m.index_of_item(self.c3)
        assert i4.row() == 0
        assert i4.column() == 0
        assert i4.parent() == i3
        i5 = self.m.index_of_item(self.c4)
        assert i5.row() == 1
        assert i5.column() == 0
        assert i5.parent() == i3
        i6 = self.m.index_of_item(self.c5)
        assert i6.row() == 0
        assert i6.column() == 0
        assert i6.parent() == i5
