"""Models for configobj objects

:class:`jukebox.core.gui.configeditor.ConfigObjModel` represents one ConfigObj and is designed for TreeViews.
:class:`jukeboxcore.gui.configeditor.InifilesModel` is designed for listviews and represents multiple ConfigObjs.
"""
from PySide import QtCore
from PySide import QtGui
from configobj import Section
from validate import Validator, ValidateError

from jukeboxcore.errors import ConfigError


class ConfigObjModel(QtCore.QAbstractItemModel):
    """Model for ConfigObj

    A ConfigObj is a tree structured ordered dictionary.
    It represents ini-Files. There can also be a config specification.
    You can validate your ConfigObj against that specification.
    The model holds the configobj and can extract data like
    keys, values, specification.
    It should be used with a tree view because you can nest sections
    inside your ini.

    The data is validated life. So invalid or valid values get different forground roles.

    The internal pointers of the indices are the sections of the ConfigObj.
    The three columns are key, value, spec.
    """

    def __init__(self, conf, parent=None):
        """Constructs a new config obj model

        :param conf: the ConfigObj with its spec already set!.
        :type conf: :class:`configobj.ConfigObj`
        :param parent: the parent object
        :type parent: :class:`PySide.QtCore.QObject`
        :returns: None
        :rtype: None
        :raises: None
        """
        super(ConfigObjModel, self).__init__(parent)
        self._conf = conf
        self._vld = Validator()
        if self._conf.configspec is not None:
            self._conf.validate(self._vld)

        # validation colors
        self._valid_col = QtGui.QColor(105, 205, 105)
        self._invalid_col = QtGui.QColor(250, 135, 135)

    def rowCount(self, parent):
        """Reimplemented from QtCore.QAbstractItemModel"""
        if not parent.isValid():
            v = self._conf
        else:
            v = self.get_value(parent)
        if isinstance(v, Section):
            return len(v.keys())
        else:
            return 0

    def columnCount(self, parent):
        """Reimplemented from QtCore.QAbstractItemModel

        3 Columns: Key, Value, Spec
        """
        return 3

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """Reimplemented from QtCore.QAbstractItemModel

        The value gets validated and is red if validation fails
        and green if it passes.
        """
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                p = index.internalPointer()
                k = self.get_key(p, index.row())
                return k
            if index.column() == 1:
                v = self.get_value(index)
                if not isinstance(v, Section):
                    return self._val_to_str(v)
            if index.column() == 2:
                return self.get_configspec_str(index)
        if role == QtCore.Qt.ForegroundRole:
            if index.column() == 1:
                v = self.get_value(index)
                if not isinstance(v, Section):
                    spec = self.get_configspec_str(index)
                    if spec is None or isinstance(spec, Section):
                        return
                    try:
                        self._vld.check(spec, v)
                    except ValidateError:
                        return QtGui.QBrush(self._invalid_col)
                    else:
                        return QtGui.QBrush(self._valid_col)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Reimplemented from QtCore.QAbstractItemModel

        You can only set the value.

        :param index: the index to edit, column should be 1.
        :type index: :class:`PySide.QtCore.QModelIndex`
        :param value: the new value for the configobj
        :type value: object
        :param role: Optional - the ItemDataRole. Default is QtCore.Qt.EditRole
        :type role: QtCore.Qt.ItemDataRole
        :returns: True if index was edited, False if index could not be edited.
        :rtype: bool
        :raises: None

        """
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                if index.column() == 1:
                    p = index.internalPointer()
                    k = self.get_key(p, index.row())
                    # we could just set the value
                    # BUT for listvalues etc it will not work
                    strval = self._val_to_str(value)
                    # _handle_value will parse it correctly
                    # comments gets lost
                    (parsedval, comment) = self._conf._handle_value(strval)
                    p[k] = parsedval
                    self.dataChanged.emit(index, index)
                    return True
        return False

    def restore_default(self, index):
        """Set the value of the given index row to its default

        :param index:
        :type index:
        :returns:
        :rtype:
        :raises:
        """
        spec = self.get_configspec_str(index)
        if spec is None or isinstance(spec, Section):
            return
        try:
            default = self._vld.get_default_value(spec)
            defaultstr = self._val_to_str(default)
            self.setData(index, defaultstr)
        except KeyError:
            raise ConfigError("Missing Default Value in spec: \"%s\"" % spec)

    def headerData(self, section, orientation, role):
        """Reimplemented from QtCore.QAbstractItemModel

        Just the header text for the 3 columns.
        Rows do not have headers.
        """
        dispheaders = ('Key', 'Value', 'Spec')
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                try:
                    return dispheaders[section]
                except IndexError:
                    return None

    def flags(self, index):
        """Reimplemented from QtCore.QAbstractItemModel

        Only the value is editable
        """
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        """Reimplemented from QtCore.QAbstractItemModel"""
        if not index.isValid():
            return QtCore.QModelIndex()
        p = index.internalPointer()
        if p is self._conf:
            return QtCore.QModelIndex()
        pp = p.parent
        pk = p.name
        row = (pp.scalars + pp.sections).index(pk)
        return self.createIndex(row, 0, pp)

    def index(self, row, column, parent):
        """Reimplemented from QtCore.QAbstractItemModel

        The internal pointer is the section.
        The row determines the key in the scalars then sections of the configobj.
        So for a given index, use row to retrieve the key::

          key = self.get_key(index.internalPointer(), index.row())

        To use the key on the section to get the value OR
        use get_value(index) / get_configspec_str

        """
        if not parent.isValid():
            s = self._conf
        else:
            p = parent.internalPointer()
            k = self.get_key(p, parent.row())
            s = p[k]
        return self.createIndex(row, column, s)

    def get_value(self, index):
        """ Return the value of the given index

        The index stores the section as internal pointer.
        The row of the index determines the key.
        The key is used on the section to return the value

        :param index: The QModelIndex
        :type index: QModelIndex
        :returns: The value for the given index
        """
        p = index.internalPointer()
        k = self.get_key(p, index.row())
        return p[k]

    def get_configspec_str(self, index):
        """ Return the config spec string of the given index

        The index stores the section as internal pointer.
        The row of the index determines the key.
        The section stores the spec in its configspec attribute
        The key is used on the configspec attribute to return the spec

        :param index: The QModelIndex
        :type index: QModelIndex
        :returns: The spec for the given index or None
        """
        p = index.internalPointer()
        if p is None:
            return
        spec = p.configspec
        if spec is None:
            return None
        k = self.get_key(p, index.row())
        try:
            return spec[k]
        except KeyError:
            return None

    def get_key(self, section, row):
        """ Return the key for the given section and row

        A sections stores scalars and sections.
        The row is the index for the combination of scalars and sections.

        :param section: A ConfigObj section
        :type section: Section
        :param row: the index for (section.scalars + section.sections)
        :type row: int
        :returns: the key
        :rtype: str
        :raises: IndexError
        """
        return (section.scalars + section.sections)[row]

    def set_valid_col(self, color):
        """Set the forgroundrole color for values if they are valid

        :param color: this color will be returned from data() when the value is valid and role is QtCore.Qt.ForegroundRole
        :type color: QtGui.QColor
        :returns: None
        :rtype: None
        :raises: None

        default is: QtGui.QColor(105, 205, 105)
        """
        self._valid_col = color

    def set_invalid_col(self, color):
        """Set the forgroundrole color for values if they are valid

        :param color: this color will be returned from data() when the value is valid and role is QtCore.Qt.ForegroundRole
        :type color: QtGui.QColor
        :returns: None
        :rtype: None
        :raises: None

        default is: QtGui.QColor(250, 135, 135)
        """
        self._invalid_col = color

    def _val_to_str(self, value):
        """Converts the value to a string that will be handled correctly by the confobj

        :param value: the value to parse
        :type value: something configobj supports
        :returns: str
        :rtype: str
        :raises: None

        When the value is a list, it will be converted to a string that can be parsed to
        the same list again.
        """
        # might be a list value
        # then represent it 'nicer' so that when we edit it, the same value will return
        if isinstance(value, list):
            # so we have a list value. the default str(v) would produce something like: ['a', 'b']
            # handling such a value is not possible. it should be: 'a', 'b'
            # so we have to convert it to a string but we have to make sure, we do not loose quotes
            # even when values are integers, they get quoted. thats alright. the config obj will parse them correctly
            return ', '.join("'%s'" % str(i) for i in value)
        return str(value)  # so we always have a line editor. validate can convert from string


class InifilesModel(QtCore.QAbstractListModel):
    """A list model for inifiles

    Stores multiple configobjs in a list that represent inifiles on the harddisk.
    """

    confobjRole = QtCore.Qt.UserRole

    def __init__(self, configs, parent=None):
        """Constructs a new model with the given ConfigObjs

        :param configs: the configobjs to display
        :type configs: list of ConfigObjs
        :param parent: the parent qobject
        :type parent: QObject
        :returns: None
        :raises: None
        """
        super(InifilesModel, self).__init__(parent)
        self.__configs = configs
        self.__edited = [False for c in self.__configs]
        self.vld = Validator()

    def rowCount(self, parent=None):
        """Reimplemented from QAbstractItemModel

        :param parent: The parent index
        :type parent: QModelIndex
        :returns: the number of configs
        :rtype: int
        :raises: None
        """
        return len(self.__configs)

    def data(self, index, role):
        """Reimplemented from QtCore.QAbstractItemModel

        :param index: the index
        :type index: QModelIndex
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: some data. for display role it returns the filename of the configobj
        :raises: None

        For display role the filename is returned.
        """
        if not index.isValid():
            return
        if role == QtCore.Qt.DisplayRole:
            conf = self.__configs[index.row()]
            edited = self.__edited[index.row()]
            if edited:
                prefix = '*'
            else:
                prefix = ''
            return '%s%s' % (prefix, conf.filename)
        if role == self.confobjRole:
            conf = self.__configs[index.row()]
            return conf

    def headerData(self, section, orientation, role):
        """Returns the data for the given role and section in the header with the specified orientation.

        :param section: the section
        :type section: int
        :param orientation: horizontal or vertical orientation
        :type orientation: QtCore.Qt.Orientation
        :param role: the datarole. default is DisplayRole
        :type role: QtCore.Qt.ItemDataRole
        :returns: headerData
        :raises: None
        """
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return 'Inifiles'

    def set_index_edited(self, index, edited):
        """Set whether the conf was edited or not.

        Edited files will be displayed with a \'*\'

        :param index: the index that was edited
        :type index: QModelIndex
        :param edited: if the file was edited, set edited to True, else False
        :type edited: bool
        :returns: None
        :rtype: None
        :raises: None
        """
        self.__edited[index.row()] = edited
        self.dataChanged.emit(index, index)

    def get_edited(self, ):
        """Return all indices that were modified

        :returns: list of indices for modified confs
        :rtype: list of QModelIndex
        :raises: None
        """
        modified = []
        for i in range(len(self.__edited)):
            if self.__edited[i]:
                modified.append(self.__configs[i])
        return modified

    def validate(self, index):
        """Validate the conf for the given index

        :param index: the index of the model to validate
        :type index: QModelIndex
        :returns: True if passed and a False/True dict representing fail/pass. The structure follows the configobj. If the configobj does not have a configspec True is returned.
        :rtype: True|Dict
        :raises: None
        """
        c = self.__configs[index.row()]
        if c.configspec is None:
            return True
        else:
            return c.validate(self.vld)
