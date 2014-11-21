"""This module features classes and interfaces to track references and loaded data and manipulate it.

It is the main lib for the reference workflow of the pipeline.
It revoles around a :class:`Reftrack`
:class:`Reftrack` object which stores all necessary information of one entity.
To interact with the programm, :class:`Reftrack` uses two interfaces.
The first is responsible create, delete, edit and query an object in your programm which
represents the entity. For example in Maya, one would create a special node, that stores information about
an entity. The interface interacts with this node and delivers the data to the :class:`Reftrack` object.
Depending on the type of the entity (e.g. an Asset, Alembic, Shader, Camera etc) a second interface
is used for actions like referencing, loading, unloading, importing, deleting the actual content of the entity.
E.g. for shaders you might want to assing them to objects on load.
"""


class Reftrack(object):
    """Represents one entity of the reference workflow in a programm

    Stores information like the status, options for replacing the entity etc.
    Delegates actions to the appropriate interfaces.
    So no matter what kind of programm  you are in and type your entity is, the :class:`Reftrack` object
    can carry out all actions as long as you provide 2 interfaces.

    A refobj interface will interact will query information about the entity and can create
    a new refobj, which will store the information in the scene. E.g. in Maya it might be a node
    which has a connection to the reference node, stores the type of the entity etc.
    The refobj interface is responsible for creating, editing, deleting the refobj.
    The refobj interface can query the reftrack object which element the entity represents (which Shot or Asset).

    The typ interface is programm and type specific. It manipulates the actual content of the entity.
    E.g. it will assign shaders upon loading, create references, connect nodes or group the referenced
    objects.

    The reftrack has 3 different statuses:

       :uptodate: If the current loaded version is the newest (does not consider other departments!)
       :alien: If the reftrack does not belongs to the currently open scene and is not linked as such in the database.
       :status: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`, None (If there is no refobj in the scene)
    """

    LOADED = "Loaded"
    """Status for when the entity is referenced in the scene and the reference is loaded."""

    UNLOADED = "Unloaded"
    """Status for when the entity is referenced but the reference is not loaded into the scene."""

    IMPORTED = "Imported"
    """Status for when the entity is imported."""

    def __init__(self, refobjinter, refobj=None, typ=None, element=None, parent=None):
        """Initialize a new container with a reftrack object interface and either a reftrack object
        or typ, element, and an optional parent.

        :param refobjinter: a programm specific reftrack object interface
        :type refobjinter: :class:`RefobjInterface`
        :param refobj: a physical representation in your scene of the entity, if it already exists.
                         If you do not specify a reftrack object, then you have to provide at least a typ and element.
                         The refobj type does not matter as long as your reftrack object interface can handle it.
        :param typ: the type of the entity (e.g. Asset, Alembic, Camera etc.). If no refobject is given, this is required
        :type typ: str
        :param element: the element the entity represents, e.g. an Asset or a Shot.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :param parent: the parent :class:`Reftrack` object. All children will be deleted automatically, when the parent gets deleted.
        :type parent: :class;`Reftrack`
        :raises: TypeError
        """
        if not (refobj or (typ and element)):
            raise TypeError("Please provide either a refobj or a typ and element.")
        if refobj and (parent or typ or element):
            raise TypeError("Refobject given. Providing a typ, element or parent is invalid. \
The Refobject provides the necessary info.")
        self._refobjinter = refobjinter
        self._typinter = None
        self._refobj = None
        self._taskfileinfo = None  # the taskfileinfo that the refobj represents
        self._typ = None
        self._element = None
        self._parent = None
        self._children = []
        self._options = None  # tree model of possible files to load
        self._uptodate = None
        self._alien = True
        self._status = None

        # initialize reftrack
        self.set_refobject(refobj)
        if not refobj:
            self.set_typ(typ)
            self.set_element(element)
            self.set_parent(parent)

    def get_refobj(self, ):
        """Return the reftrack object, the physical representation of your :class:`Reftrack` object in the scene.
        If the entity is not loaded, None is returned

        :returns: the reftrack object
        :rtype: None | reftrack object
        :raises: None
        """
        return self._refobj

    def set_refobj(self, refobj):
        """Set the reftrack object.

        The reftrack object interface will determine typ, element, taskfileinfo, status and parent and set these values.
        If the reftrack object is None, the :class:`Reftrack` object will keep the initial typ,
        element but will loose it\'s parent, status and taskfileinfo

        :param refobj: a reftrack object or None
        :type refobj: None | reftrack object
        :returns: None
        :rtype: None
        :raises: None
        """
        self._refobj = refobj
        refobjinter = self.get_refobjinter()
        if self._refobj:
            self.set_typ(refobjinter.get_typ(self._refobj))
            self.set_taskfileinfo(refobjinter.get_taskfileinfo(self._refobj))
            self.set_element(refobjinter.get_element(self._refobj))
            self.set_parent(refobjinter.get_parent(self._refobj))
            self.set_status(refobjinter.get_status(self._refobj))
        else:
            self.set_taskfileinfo(None)
            self.set_parent(None)
            self.set_status(None)
        self.fetch_uptodate()

    def get_typ(self, ):
        """Return the type of the entity

        E.g. Asset, Alembic, Camera etc

        :returns: the type of the entity
        :rtype: str
        :raises: None
        """
        return self._typ

    def set_typ(self, typ):
        """Set the type of the entity

        This will set the typ_interface of the :class:`Reftrack` instance

        :param typ: the type of the entity
        :type typ: str
        :returns: None
        :rtype: None
        :raises: None
        """
        self._typ = typ
        self._typinter = self.get_refobjinter().get_typinter(typ)

    def get_typinter(self, ):
        """Return the type interface

        The type interface is responsible for manipulating the content of the entity.
        Depending on the typ it will assing shaders, group objects etc.

        :returns: the type interface
        :rtype: :class:`ReftypeInterface`
        :raises: None
        """
        return self._typinter

    def get_refobjinter(self, ):
        """Return the refobject interface

        :returns: the refobject interface
        :rtype: :class:`RefobjInterface`
        :raises: None
        """
        return self._refobjinter

    def get_taskfileinfo(self, ):
        """Return the :class:`jukeboxcore.filesys.TaskFileInfo` that the refobject represents.

        :returns: the taskfileinfo for the refobject or None if nothing is loaded.
        :rtype: :class:`jukeboxcore.filesys.TaskFileInfo` | None
        :raises: None
        """
        return self._taskfileinfo

    def set_taskfileinfo(self, tfi):
        """Set the :class:`jukeboxcore.filesys.TaskFileInfo` that the refobject represents.

        :param tfi: the taskfileinfo for the refobject or None if nothing is loaded.
        :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        self._taskfileinfo = tfi
        if tfi:
            self.set_element(tfi.task.element)

    def get_element(self, ):
        """Return the element the reftrack represents.

        The element is either an Asset or a Shot.
        Depending on the type only certain files are considered for loading
        or referencing.

        :returns: The element the reftrack represents
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        return self._element

    def set_element(self, element):
        """Set the element for the reftrack to represent.

        The element is either an As

        The element is either an Asset or a Shot.
        Depending on the type only certain files are considered for loading
        or referencing.
        This will also set the available options and set the alien status.

        :param element: The element the reftrack represents.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._element = element
        self.fetch_options()
        self.fetch_alien()

    def get_parent(self, ):
        """Return the parent :class:`Reftrack` instance

        :returns: None
        :rtype: :class:`Reftrack` | None
        :raises: None
        """
        return self._parent

    def set_parent(self, parent):
        """Set the parent reftrack object

        If a parent gets deleted, the children will be deleted too.

        .. Note:: Adds the instance to the children of the parent
                  and removes it from the old parent

        :param parent: the parent reftrack object
        :type parent: :class:`Reftrack` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        oldparent = self._parent
        if oldparent:
            oldparent.removeChild(self)
        self._parent = parent
        if parent:
            self._parent.addChild(self)

    def addChild(self, reftrack):
        """Add the given reftrack object as child

        .. Note:: Does not set the parent of the child!

        :param reftrack: the child :class:`Reftrack` instance
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._children.append(reftrack)

    def removeChild(self, reftrack):
        """Remove the given reftrack from children

        .. Note:: Does not set the parent of the child to None!

        :param reftrack: the child :class:`Reftrack` instance
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: ValueError
        """
        self._children.remove(reftrack)

    def get_options(self, ):
        """Return a :class:`jukeboxcore.gui.treemodel.Treemodel` with possible options
        for the reftrack to load, replace, import etc.

        The leafes of the :class:`jukeboxcore.gui.treemodel.Treemodel`
        should be TreeItems with TaskFileInfo as internal data.

        :returns: a treemodel with options
        :rtype: :class:`jukeboxcore.gui.treemodel.Treemodel`
        :raises: None
        """
        return self._options

    def fetch_options(self, ):
        """Set and return the options for possible files to
        load, replace etc. The stored element will determine the options.

        The typinterface is responsible for providing the options

        :returns: the options
        :rtype: :class:`jukeboxcore.gui.treemodel.Treemodel`
        :raises: None
        """
        self._options = self.get_typinter().fetch_options(self._element)
        return self._options

    def uptodate(self, ):
        """Return True, if the currently loaded entity is the newest version.
        Return False, if there is a newer version.
        Return None, if there is no current scene object.

        :returns: whether the reftrack is uptodate
        :rtype: bool | None
        :raises: None
        """
        return self._uptodate

    def fetch_uptodate(self, ):
        """Set and return whether the currently loaded entity is
        the newest version in the department.

        :returns: True, if newest version. False, if there is a newer version.
                  None, if there is nothing loaded yet.
        :rtype: bool | None
        :raises: None
        """
        tfi = self.get_taskfileinfo()
        if tfi:
            self._uptodate = tfi.isLatest()
        else:
            self._uptodate = None
        return self._uptodate

    def alien(self, ):
        """Return True, if the reftrack element is not linked to the current scene

        :returns: whether the element is linked to the current scene
        :rtype: bool
        :raises: None
        """
        return self._alien

    def fetch_alien(self, ):
        """Set and return, if the reftrack element is linked to the current scene.

        Askes the refobj interface for the current scene.
        If there is no current scene then True is returned.

        :returns: whether the element is linked to the current scene
        :rtype: bool
        :raises: None
        """
        current = self.get_refobjinter().get_current_element()
        if not current:
             self._alien = True
        else:
            assets = current.assets
            self._alien = self.get_element() not in assets
        return self._alien

    def status(self, ):
        """Return the status of the reftrack

        The status indicates, whether the entity is loaded, unloaded etc.
        None if there is no refobj in the scene.

        See: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`.

        :returns: the status
        :rtype: str | None
        :raises: None
        """
        return self._status

    def set_status(self, status):
        """Set the status of the reftrack

        The status indicates, whether the entity is loaded, unloaded etc.
        None if there is no refobj in the scene.

        See: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`.

        :param status: the status
        :type status: str | None
        :returns: None
        :rtype: None
        :raises: None
        """
        self._status = status

    def create_refobject(self, ):
        """Create a refobject that represents the :class:`Reftrack` instance.

        .. Note:: This will not set the reftrack object.

        :returns: the created reftrack object
        :rtype: scene object
        :raises: None
        """
        refobj = self.get_refobjinter().create_refobject(self.get_typ(), self.get_parent())
        return refobj

    def reference(self, taskfileinfo):
        """Reference the entity into the scene. Only possible if the current status is None

        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() is None,\
            "Can only reference, if the entity is not already referenced/imported. Use replace instead."
        refobj = self.get_refobjinter().create(self.get_typ(), self.get_parent())
        self.get_typinter().reference(taskfileinfo, refobj)
        self.set_refobj(refobj)

    def load(self, ):
        """If the reference is in the scene but unloaded, load it.

        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() == self.UNLOADED,\
            "Cannot load if there is no unloaded reference. Use reference instead."
        self.get_typinterface().load(self._refobj)
        self.set_status(self.LOADED)

    def unload(self, ):
        """If the reference is loaded, unload it.

        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() == self.LOADED,\
            "Cannot unload if there is no loaded reference. \
Use delete if you want to get rid of a reference or import."
        self.get_typinterface().unload(self._refobj)
        self.set_status(self.UNLOADED)

    def import_entity(self, taskfileinfo=None):
        """Import the entity.

        :param taskfileinfo: the taskfileinfo to import. If None is given, try to import
                             the current reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() is not self.IMPORTED,\
            "Entity is already imported. Use replace instead."
        typinter = self.get_typinter()
        if self.status() is None:
            assert taskfileinfo,\
                "Can only import an already referenced entity \
or a given taskfileinfo. No taskfileinfo was given though"
            refobj = self.get_refobjinter().create(self.get_typ(), self.get_parent())
            typinter.import_taskfile(taskfileinfo, refobj)
            self.set_refobj(refobj)
        else:
            typinter.import_reference(self.get_refobj())
        self.set_status(self.IMPORTED)

    def replace(self, taskfileinfo):
        """Replace the current reference or imported entity.

        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() is not None,\
            "Can only replace entities that are already in the scene."
        typinter = self.get_typinter()
        if typinter.is_replaceable(self.get_refobj()):
            typinter.replace(taskfileinfo)
            self.fetch_uptodate()
        else:
            status = self.status()
            self.delete()
            if status == self.IMPORTED:
                self.import_entity(taskfileinfo)
            else:
                self.reference(taskfileinfo)

    def delete(self, ):
        """Delete the current entity.

        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() is not None,\
            "Can only delete entities that are already in the scene."
        refobjinter = self.get_refobjinter()
        refobjs = refobjinter.get_children_to_delete(self.get_refobj())
        refobjs.append(self.get_refobj())
        for r in refobjs:
            refobjinter.delete(r)
        self.set_refobj(None)
        if self.alien():
            self.get_parent().removeChild(self)
        else:
            self._children = []

    def duplicate(self, ):
        """Return a new :class:`Reftrack` instance that has the same
        typ, element and parent. The new reference will be unloaded!

        :returns: a new reftrack instance with same typ, element and parent
        :rtype: :class:`Reftrack`
        :raises: None
        """
        return self.__class__(self.get_refobjinter(), typ=self.get_typ(), element=self.get_element(), parent=self.get_parent())
