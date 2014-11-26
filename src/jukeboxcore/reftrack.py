"""This module features classes and interfaces to track references and loaded data and manipulate it.

It is the main lib for the reference workflow of the pipeline.
It revoles around a :class:`Reftrack` object.
Each :class:`Reftrack` instance is responsible for one entity.
It holds information about the entity, can query the entity and manipulate the entity.

One entity might be a character asset, an alembic cache for the character, a camera or a lightrig.
The :class:`Reftrack` instance can reference, load, unload, import, replace or delete the entity.
Once an entity is loaded into your programm, the :class:`Reftrack` object holds a refobject.

A refobject can be anything, from a node that is in your programm, to a simple string.
Important is, that it can be used by the :class:`RefobjInterface` to identify the entity in your scene
and query information. E.g. in Maya, one would create a special Node for each loaded entity.
The node can be used to query the reference status, it can identify what entity is loaded etc.
So in this case the refobj would be either the node, or the name of the node. Whatever your :class:`RefobjInterface`
accepts.

Again, the :class:`RefobjInterface` is used to identify the entity, query the parent, status, create new refobjects
and manipulate them. It is specific for each software you use. So there should be one implementation of the
:class:`RefobjInterface` for each software. The :class:`Reftrack` object will interact with the interface
to manipulate the scene.

Each entity has a certain type. For example one type might be ``"Asset"`` and another might be ``"Shader"``.
Depending on the type and of course the software you are in (or in this case simply the :class:`RefobjInterface`),
you want to perform different actions on loading or deleting the entity. E.g. when loading a shader, you might want
to apply the shaders to another entity etc. Or for each type you have special nodes in your software you want to use.
The :class:`Reftrack` object simply asks the :class:`RefobjInterface` to reference, load, delete or whatever the entity.
The :class:`RefobjInterface` will decide upon the type of the :class:`Reftrack` to use another interface.
This interface is called :class:`ReftypeInterface`.

The :class:`ReftypeInterface` should be implemented for each type of entities for each software. So if your software
supports assets, shaders and alembic caches as types then you need 3 implementations of the :class:`ReftypeInterface`
for this software. The interface actually manipulates the content of the entity. For example, in Maya it will
create a reference node and group the loaded data under a transform node for assets. For shaders it might also assing the
shaders to certain objects. Make sure that your :class:`ReftypeInterface` classes are registered at the appropriate
:class:`RefobjInterface`. Use the classmethod :meth:`RefobjInterface.register_type` on your refobj interface subclass
or but them directly in :data:`RefobjInterface.types` when defining the class.

Each :class:`Reftrack` object can have a parent. A parent is another :class:`Reftack` object and is responsible
for its children. If the parent is deleted, all other children should be deleted too. This might be the case for a shader.
Imagine assigning a shader to an asset. The asset would be the parent and the shader the child. If the asset gets deleted
the shader should be deleted to. Of course, if the shader is already referenced in the asset, it will get deleted automaitcally.
The :class:`Reftrack` objects handle such cases by themselves.

There is also a :class:`ReftrackRoot` class. It is important to group all reftracks of your current scene under the same root.
The root object is mainly used to find parent :class:`Reftrack` objects. But it also provides a Qt model that you can use
for views. It holds all :class:`Reftrack` objects in a tree model.

You can create a :class:`Reftrack` objects on two ways.

  First case would be, you have a scene with refobjs. This would mean, you want to wrap all refobjs in a :class:`Reftrack` object.
  There is only a slight problem. If you want to wrap a refobj that defines a shader and has a parent refobj (e.g. an asset) you
  cannot create set the parent on initialisation, beacause the parent refobj might not be wrapped in a :class:`Reftrack` object.
  So you have to wrap all refobjs first, and in a second step find the parent :class:`Reftrack` and set it.
  For convenience, there is a class method :meth:`Reftrack.wrap`. It wraps all refobjs and finds the parents afterwards.
  This is also why the :class:`ReftrackRoot` is so important.

  The second case would be, you want to add a new :class:`Reftrack` that is not in your scene. The user would see, that it is
  not loaded and could choose to reference it or import it. In this case you initialize a :class:`Reftrack` with a type, element and parent.
  The type is for example ``"Shader"``. The element would be either a Shot or Asset in your database. So you would choose the character asset.
  The parent would be an already existing :class:`Reftrack` of the character asset with type ``"Asset"``. In other cases, you do not need a parent.
  E.g. you create a new :class:`Reftrack` for the character asset. It would have no parent.

If you have implementations for each interface, it should be fairly easy to use:

  Create a new :class:`RefobjInterface` instance::

    refobjinter = RefobjInterface()  # use a subclass that implemented the abstract methods here.

  Create a new :class:`ReftrackRoot` instance. It needs a root :class:`jukeboxcore.gui.treemodel.TreeItem` for the model and and
  a :class:`jukeboxcore.gui.treemodel.ItemData` subclass to create new items. The item data subclass should accept a :class:`Reftrack` object
  for the initialisation and returns data for several attributes of the :class:`Reftrack` instance.
  You do not have to specify a rootitem or itemdataclass necessarily. If you do not the root object will create standard ones.
  Only if you need custom ones you can specify them::

    from jukeboxcore.gui.treemodel import TreeItem, ListItemData
    rootdata = ListItemData(["Name", "Status", "Version"])  # root data will be used for headers in views
    rootitem = TreeItem(rootdata)
    reftrackroot = ReftrackRoot(rootitem, myitemdataclass)  # use your ItemData subclass here.

  Now lets create new :class:`Reftrack` instances. First lets create a reftrack for every refobj in the current scene::

    # get all refobjs in the scene
    refobjs = refobjinter.get_all_refobjs()
    # wrap them in reftrack instances
    reftracks = Reftrack.wrap(reftrackroot, refobjinter, refobjs)

  Done. Now to display that in a view you can get the model of the root::

    model = reftrackroot.get_model()
    # set it on a view. we assume you already have a subclass of QtGui.QAbstractItemView
    view.setModel(model)

  Now lets say the scene is incomplete. You want to add a new asset (e.g. a tree asset) to the scene.
  First we need to create a :class:`Reftrack` object::

    # get the tree asset from the database
    tree = ...
    reftrack = Reftrack(reftrackroot, refobjinter, typ="Asset", element=tree, parent=None)

  The model will get updated automatically and the view should automatically update. Lets say you want to
  reference the tree into your scene. An asset has different deparments or tasks and in each task there are
  multiple releases. Each :class:`Reftrack` object can give you options from which to choose a file to load or replace.
  The options are a :class:`jukeboxcore.gui.treemodel.TreeModel` with :class:`jukeboxcore.filesys.TaskFileInfo` as leafes.
  I explicitly say leafes because the options might be sorted in a tree like strucure. So the user could first select a task
  and then the apropriate release.
  You can take the model and display it to the user so he can select a file.::

    # get the treemodel for the options
    options = reftrack.get_options()
    # put it in another view
    optionsview.setModel(options)
    # let the user select a option
    # get the selected index (make sure it is a leaf)
    sel = optionsview.selectedIndexes()
    # sel might be a empty list if the user has not made an selection!
    # but lets assume he has selected one index
    index = sel[0]
    # get the TaskFileInfo for this index.
    taskfileinfo = index.internalPointer().internal_data()
    reftrack.reference(taskfileinfo)

So before you start, here is a list of things to do:

  1. Implement a :class:`ReftypeInterface` for each type.
  2. Implement :class:`RefobjInterface`. Make sure it has
     all the types registered. See :meth:`RefobjInterface.register_type`.
  3. Think about creating your custom :class:`jukeboxcore.gui.treemodel.ItemData`
     for :class:`Reftrack` objects.
  4. Create a :class:`RefobjInterface` instance.
  5. Create a :class:`ReftrackRoot` instance.
  6. For refobjs in your scene use :meth:`Reftrack.wrap`.
  7. Add new reftracks.

"""
import abc

from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.treemodel import TreeModel, TreeItem


class ReftrackRoot(object):
    """Groups a collection of :class:`Reftrack` objects.

    Enables the search for parents via the refobject.
    Provides a :class:`jukeboxcore.gui.treemodel.TreeModel` that can be used
    in views, to display all reftracks.

    """
    def __init__(self, rootitem, itemdataclass):
        """Initialize a new Reftrack root with a given root tree item and
        a :class:`jukeboxcore.gui.treemodel.ItemData` class to wrap
        the :class:`Reftrack` objects.

        The ItemData class should accept a :class:`Reftrack` object as
        first argument in the constructor.

        :param rootitem: the root tree item for the treemodel.
                         The root tree item will be responsible for the headers in a view.
        :type rootitem: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :param itemdataclass: the itemdata subclass to be used for wrapping the :class:`Reftrack` objects
                              in the model. Not an instance! A class! The constructor should accept
                              a :class:`Reftrack` object as first argument.
        :type itemdataclass: :class:`jukebox.core.gui.treemodel.ItemData`
        :raises: None
        """
        self._model = TreeModel(rootitem)
        self._rootitem = rootitem
        self._idataclass = itemdataclass
        self._reftracks = set()  # a list of all reftracks in belonging to the root
        self._parentsearchdict = {}
        """Keys are the refobjs of the Reftrack and the values are the Reftrack objects.
        So you can easily find the parent Reftrack for a parent refobj.
        """

    def get_model(self, ):
        """Return the treemodel that contains all reftracks of this root

        :returns: The treemodel
        :rtype: :class:`TreeModel`
        :raises: None
        """
        return self._model

    def get_rootitem(self, ):
        """Return the rootitem of the treemodel

        :returns: the rootitem
        :rtype: :class:`TreeItem`
        :raises: None
        """
        return self._rootitem

    def add_reftrack(self, reftrack):
        """Add a reftrack object to the root.

        This will not handle row insertion in the model!

        :param reftrack: the reftrack object to add
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._reftracks.add(reftrack)
        refobj = reftrack.get_refobj()
        if refobj:
            self._parentsearchdict[refobj] = reftrack

    def remove_reftrack(self, reftrack):
        """Remove the reftrack from the root.

        This will not handle row deletion in the model!

        :param reftrack: the reftrack object to remove
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._reftrack.remove(reftrack)
        refobj = reftrack.get_refobj()
        if refobj and refobj in self._parentsearchdict:
            del self._parentsearchdict[refobj]

    def update_refobj(self, old, new, reftrack):
        """Update the parent search dict so that the reftrack can be found
        with the new refobj and delete the entry for the old refobj

        :param old: the old refobj of reftrack
        :param new: the new refobj of reftrack
        :param reftrack: The reftrack, which refobj was updated
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        if old:
            del self._parentsearchdict[old]
        if new:
            self._parentsearchdict[new] = reftrack

    def get_reftrack(self, refobj):
        """Return a the Reftrack instance that wraps around the given
        refobj

        :param refobj: a ref object. See :meth:`Reftrack.get_refobj`
        :returns: The reftrack instance that wraps the given refobj.
                  If no instance is found in this root, a KeyError is raised.
        :rtype: :class:`Reftrack`
        :raises: :class:`KeyError`
        """
        return self._parentsearchdict[refobj]

    def create_itemdata(self, reftrack):
        """Return a itemdata for the given reftrack

        :param reftrack: the reftrack to wrap in a itemdata
        :type reftrack: :class:`Reftrack`
        :returns: a Itemdata with the reftrack wrapped. The ItemData class depends on what was provided for
                  initialisation of the root.
        :rtype: :class:`jukeboxcore.gui.treemodel.ItemData`
        :raises: None
        """
        return self._idataclass(reftrack)


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

    def __init__(self, root, refobjinter, typ=None, element=None, parent=None, refobj=None):
        """Initialize a new container with a reftrack object interface and either a reftrack object
        or typ, element, and an optional parent.

        .. Warning:: If you initialize with typ, element and parent, never set the parent
                     later.
                     Only when you provide a refobj, you should call :meth:`Reftrack.set_parent`
                     after you created all :class:`Reftrack` objects for all refobjs in your scene.
                     In this case it is adviced to use :meth:`Reftrack.wrap`

        :param root: the root that groups all reftracks and makes it possible to search for parents
        :type root: :class:`ReftrackRoot`
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
        :type parent: :class:`Reftrack` | None
        :raises: TypeError
        """
        if not (refobj or (typ and element)):
            raise TypeError("Please provide either a refobj or a typ and element.")
        if refobj and (parent or typ or element):
            raise TypeError("Refobject given. Providing a typ, element or parent is invalid. \
The Refobject provides the necessary info.")
        self._root = root
        self._refobjinter = refobjinter
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
        self._treeitem = None  # a treeitem for the model of the root
        """A treeitem for the model of the root. Will get set when parents gets set!"""

        # initialize reftrack
        if not refobj:
            self.set_typ(typ)
            self.set_element(element)
            self.set_parent(parent)
        else:
            self.set_typ(refobjinter.get_typ(self._refobj))
            self.set_taskfileinfo(refobjinter.get_taskfileinfo(self._refobj))
            self.set_element(refobjinter.get_element(self._refobj))
            self.set_status(refobjinter.get_status(self._refobj))
            root.update_refobj(None, refobj, self)
            self.fetch_uptodate()

        self._root.add_reftrack(self)

    @classmethod
    def wrap(cls, root, refobjinter, refobjects):
        """Wrap the given refobjects in a :class:`Reftrack` instance
        and set the right parents

        :param refobjects: list of refobjects
        :type refobjects: list
        :returns: list with the wrapped :class:`Reftrack` instances
        :rtype: list
        :raises: None
        """
        tracks = []
        for r in refobjects:
            track = cls(root=root, refobjinter=refobjinter, refobj=r)
            tracks.append(track)
        for t in tracks:
            parentrefobj = refobjinter.get_parent(t._refobj)
            parentreftrack = root.get_reftrack(parentrefobj)
            t.set_parent(parentreftrack)
        return tracks

    def get_root(self, ):
        """Return the ReftrackRoot this instance belongs to

        :returns: the root
        :rtype: :class:`ReftrackRoot`
        :raises: None
        """
        return self._root

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
        root = self.get_root()
        old = self._refobj
        self._refobj = refobj
        refobjinter = self.get_refobjinter()
        if self._refobj:
            self.set_typ(refobjinter.get_typ(self._refobj))
            self.set_taskfileinfo(refobjinter.get_taskfileinfo(self._refobj))
            self.set_element(refobjinter.get_element(self._refobj))
            parentrefobj = refobjinter.get_parent(self._refobj)
            parentreftrack = root.get_reftrack(parentrefobj)
            self.set_parent(parentreftrack)
            self.set_status(refobjinter.get_status(self._refobj))
        else:
            self.set_taskfileinfo(None)
            self.set_parent(None)
            self.set_status(None)
        root.update_refobj(old, refobj, self)
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

        :param typ: the type of the entity
        :type typ: str
        :returns: None
        :rtype: None
        :raises: None
        """
        self._typ = typ

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

        .. Note:: Once the parent is set, it cannot be set again!

        :param parent: the parent reftrack object
        :type parent: :class:`Reftrack` | None
        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self._parent is None,\
            "Cannot change the parent. Can only set from None."
        self._parent = parent
        if parent:
            refobjinter = self.get_refobjinter()
            refobj = self.get_refobj()
            # set the parent of the refobj only if it is not already set
            # and only if there is one! oO
            if refobj and not refobjinter.get_parent(refobj):
                refobjinter.set_parent(refobj, parent.get_refobj())
            # add to parent
            self._parent.add_child(self)
        self._treeitem = self.create_treeitem()

    def create_treeitem(self, ):
        """Create a new treeitem for this reftrack instance.

        .. Note:: Parent should be set, Parent should already have a treeitem.
                  If there is no parent, the root tree item is used as parent for the treeitem.

        :returns: a new treeitem that contains a itemdata with the reftrack instanec.
        :rtype: :class:`TreeItem`
        :raises: None
        """
        p = self.get_parent()
        root = self.get_root()
        if p:
            pitem = p.get_treeitem()
            assert pitem, "No TreeItem was set in the parent!"
        else:
            pitem = root.get_rootitem()
        idata = root.create_itemdata(self)
        return TreeItem(idata, parent=pitem)

    def get_treeitem(self, ):
        """Return the treeitem that wraps this instance.

        There is only a treeitem if the parent has been set once.

        :returns: the treeitem for this instance
        :rtype: :class:`TreeItem` | None
        :raises: None
        """
        return self._treeitem

    def add_child(self, reftrack):
        """Add the given reftrack object as child

        .. Note:: Does not set the parent of the child!

        :param reftrack: the child :class:`Reftrack` instance
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._children.append(reftrack)

    def remove_child(self, reftrack):
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
        """Return a :class:`jukeboxcore.gui.treemodel.TreeModel` with possible options
        for the reftrack to load, replace, import etc.

        The leafes of the :class:`jukeboxcore.gui.treemodel.TreeModel`
        should be TreeItems with TaskFileInfo as internal data.

        :returns: a treemodel with options
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        return self._options

    def fetch_options(self, ):
        """Set and return the options for possible files to
        load, replace etc. The stored element will determine the options.

        The refobjinterface and typinterface are responsible for providing the options

        :returns: the options
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        self._options = self.get_refobjinter().fetch_options(self.get_typ(), self._element)
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
        refobjinter = self.get_refobjinter()
        refobj = refobjinter.create(self.get_typ(), self.get_parent())
        refobjinter.reference(taskfileinfo, refobj)
        self.set_refobj(refobj)

    def load(self, ):
        """If the reference is in the scene but unloaded, load it.

        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        assert self.status() == self.UNLOADED,\
            "Cannot load if there is no unloaded reference. Use reference instead."
        self.get_refobjinter().load(self._refobj)
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
        self.get_refobjinter().unload(self._refobj)
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
        refobjinter = self.get_refobjinter()
        if self.status() is None:
            assert taskfileinfo,\
                "Can only import an already referenced entity \
or a given taskfileinfo. No taskfileinfo was given though"
            refobj = self.get_refobjinter().create(self.get_typ(), self.get_parent())
            refobjinter.import_taskfile(refobj, taskfileinfo)
            self.set_refobj(refobj)
        else:
            refobjinter.import_reference(self.get_refobj())
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
        refobjinter = self.get_refobjinter()
        refobj = self.get_refobj()
        if refobjinter.is_replaceable(refobj):
            refobjinter.replace(refobj, taskfileinfo)
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
            self.get_parent().remove_child(self)
            # remove from root
            root = self.get_root()
            root.remove_reftrack(self)
            self._treeitem.parent().remove_child(self._treeitem)
        else:
            for c in self._children:
                self._treeitem.remove_child(c._treeitem)
            self._children = []

    def duplicate(self, ):
        """Return a new :class:`Reftrack` instance that has the same
        typ, element and parent. The new reference will be unloaded!

        :returns: a new reftrack instance with same typ, element and parent
        :rtype: :class:`Reftrack`
        :raises: None
        """
        return self.__class__(root=self.get_root(),
                              refobjinter=self.get_refobjinter(),
                              typ=self.get_typ(),
                              element=self.get_element(),
                              parent=self.get_parent())


class RefobjInterface(object):
    """Interface to interact with a reference object that is in your scene.

    This interface is abstract. You should implement it for every software where you need
    a reference workflow.
    To interact with the content of each entity, there is a special reftyp interface that
    is not only software specific but also handles only a certain type of entity.
    You can register additional type interfaces, so plugins can introduce their own entity types.

    Methods to implement:

      * :meth:`RefobjInterface.get_parent`
      * :meth:`RefobjInterface.set_parent`
      * :meth:`RefobjInterface.get_children`
      * :meth:`RefobjInterface.get_typ`
      * :meth:`RefobjInterface.set_typ`
      * :meth:`RefobjInterface.create_refobj`
      * :meth:`RefobjInterface.referenced`
      * :meth:`RefobjInterface.delete_refobj`
      * :meth:`RefobjInterface.get_all_refobj`
      * :meth:`RefobjInterface.get_current_element`
      * :meth:`RefobjInterface.set_reference`
      * :meth:`RefobjInterface.get_reference`
      * :meth:`RefobjInterface.get_status`
      * :meth:`RefobjInterface.get_taskfile`

    """

    types = {}
    """A dictionary that maps types of entities (strings) to the reftypinterface class"""

    def __init__(self, ):
        """Initialize a new refobjinterface.

        :raises: None
        """
        pass

    @classmethod
    def register_type(cls, typ, interface):
        """Register a new typ with the given interface class

        :param typ: the entity typ that you want to register
        :type typ: str
        :param interface: the interface class
        :type interface: :class:`ReftypeInterface`
        :returns: None
        :rtype: None
        :raises: None
        """
        cls.types[typ] = interface

    def get_typ_interface(self, typ):
        """Return an appropriate interface for the given entity type

        :param typ: the entity type
        :type typ: str
        :returns: a interface instance
        :rtype: :class:`ReftypeInterface`
        :raises: KeyError
        """
        return self.types[typ](self)

    @abc.abstractmethod
    def get_parent(self, refobj):
        """Return the refobj of the parent of the given refobj

        :param refobj: a reference object to query
        :type refobj: refobj
        :returns: the parent refobj
        :rtype: refobj | None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_parent(self, child, parent):
        """Set the parent of the child refobj

        :param child: the child refobject
        :type child: refobj
        :param parent: the parent refobject
        :type parent: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_children(self, refobj):
        """Get the children refobjects of the given refobject

        :param refobj: the parent refobj
        :type refobj: refobj
        :returns: a list with children refobjects
        :rtype: list
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_typ(self, refobj):
        """Return the entity type of the given refobject

        See: :data:`RefobjInterface.types`.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the entity type
        :rtype: str
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_typ(self, refobj, typ):
        """Set the type of the given refobj

        :param refobj: the refobj to query
        :type refobj: refobj
        :param typ: the entity type
        :type typ: str
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_refobj(self, ):
        """Create and return a new refobj

        :returns: the new refobj
        :rtype: refobj
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def referenced(self, refobj):
        """Return whether the given refobj is referenced.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: True if referenced, False if imported
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    def create(self, typ, parent=None):
        """Create a new refobj with the given typ and parent

        :param typ: the entity type
        :type typ: str
        :param parent: the parent refobject
        :type parent: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        refobj = self.create_refobj()
        self.set_typ(refobj, typ)
        if parent:
            self.set_parent(refobj, parent)

    @abc.abstractmethod
    def delete_refobj(self, refobj):
        """Delete the given refobj

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    def delete(self, refobj):
        """Delete the given refobj and all of it\'s children
        that should be deleted as well.

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        refobjs = self.get_children(refobj)
        refobjs = [r for r in refobjs if self.referenced(r)]
        refobjs.append(refobj)
        for r in refobjs:
            i = self.get_typ_interface(self.get_typ(r))
            i.delete(r)
            self.delete_refobj(r)

    @abc.abstractmethod
    def get_all_refobjs(self, ):
        """Return all refobjs in the scene

        :returns: all refobjs in the scene
        :rtype: list
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_element(self, ):
        """Return the currenty open Shot or Asset

        :returns: the currently open element
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot` | None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_reference(self, refobj, reference):
        """Set the reference of the given refobj to reference

        This will be called by the typinterface after the reference
        has been made. The typinterface should deliver an appropriate
        object as reference that can be used to track the reference
        in the scene. If you query refobj afterwards it should say, that
        it is referenced.

        :param refobj: the refobj to update
        :type refobj: refobj
        :param reference: the value for the refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reference(self, refobj):
        """Return the reference that the refobj represents

        E.g. in Maya this would return the linked reference node.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the reference object in the scene
        :raises: None
        """
        raise NotImplementedError

    def reference(self, taskfileinfo, refobj):
        """Reference the given taskfile info and
        set the created reference on the refobj

        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :param refobj: the refobj that should represent the new reference
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        ref = inter.reference(taskfileinfo)
        self.set_reference(refobj, ref)

    def load(self, refobj):
        """Load the given refobject

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        :param refobj: the refobject
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        ref = self.get_reference(refobj)
        inter.load(ref)

    def unload(self, refobj):
        """Load the given refobject

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        :param refobj: the refobject
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        ref = self.get_reference(refobj)
        inter.unload(ref)

    def replace(self, refobj, taskfileinfo):
        """Replace the given refobjs reference with the taskfileinfo

        :param refobj: the refobject
        :type refobj: refobj
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        ref = self.get_reference(refobj)
        inter.replace(ref, taskfileinfo)

    def is_replaceable(self, refobj):
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        return inter.is_replaceable(refobj)

    def import_reference(self, refobj):
        """Import the reference of the given refobj

        :param refobj: the refobj with a reference
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        ref = self.get_reference(refobj)
        inter.import_reference(ref)

    def import_taskfile(self, refobj, taskfileinfo):
        """Import the given taskfileinfo and update the refobj

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_type(refobj))
        inter.import_taskfile(refobj, taskfileinfo)

    @abc.abstractmethod
    def get_status(self, refobj):
        """Return the status of the given refobj

        See: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the status of the given refobj
        :rtype: str
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_taskfile(self, refobj):
        """Return the taskfile that is loaded and represented by the refobj

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: The taskfile that is loaded in the scene
        :rtype: :class:`jukeboxcore.djadapter.TaskFile`
        :raises: None
        """
        raise NotImplementedError

    def get_taskfileinfo(self, refobj):
        """Return the :class:`jukeboxcore.filesys.TaskFileInfo` that is loaded
        by the refobj

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: the taskfileinfo that is loaded in the scene
        :rtype: :class:`jukeboxcore.filesys.TaskFileInfo`
        :raises: None
        """
        tf = self.get_taskfile(refobj)
        return TaskFileInfo(task=tf.task,
                            version=tf.version,
                            releasetype=tf.releasetype,
                            typ=tf.typ,
                            descriptor=tf.descriptor)

    def fetch_options(self, typ, element):
        """Fetch the options for possible files to
        load replace etc for the given element.

        :param typ: the typ of options. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: the options
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        inter = self.get_typ_interface(typ)
        return inter.fetch_options(element)


class ReftypeInterface(object):
    """Interface for manipulating the content of an entity in the scene

    This interface is abstract. You should implement it for every software and
    type where you need a reference workflow.
    The ReftypeInterface is responsible for the main reference workflow actions
    like loading, referencing and importing.
    Depending on the type of your entity, additional actions may be appropriate.
    E.g. if the type is a shader, then you might want to assign the shader
    to the parent of the shader refobject.

    Methods to implement:

      * :meth:`ReftypeInterface.reference`
      * :meth:`ReftypeInterface.load`
      * :meth:`ReftypeInterface.unload`
      * :meth:`ReftypeInterface.replace`
      * :meth:`ReftypeInterface.delete`
      * :meth:`ReftypeInterface.import_reference`
      * :meth:`ReftypeInterface.import_taskfile`
      * :meth:`ReftypeInterface.is_replaceable`
      * :meth:`ReftypeInterface.fetch_options`

    """

    def __init__(self, refobjinter):
        """Initialize a new ReftypeInterface

        :param refobjinter: the refobject interface
        :type refobjinter: :class:`RefobjInterface`
        :raises: None
        """
        self._refobjinter = refobjinter

    def get_refobjinter(self, ):
        """Return the :class:`RefobjInterface` that initialized the interface

        :returns: the refobj interface that initialized the interface
        :rtype: :class:`RefobjInterface`
        :raises: None
        """
        return self._refobjinter

    @abc.abstractmethod
    def reference(self, taskfileinfo):
        """Reference the given taskfileinfo into the scene and return the created reference object

        The created reference object will be used on :meth:`RefobjInterface.set_reference` to
        set the reference on a refobj. E.g. in Maya, one would return the reference node
        so the RefobjInterface can link the refobj with the refernce object.

        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: the reference that was created and should set on the appropriate refobj
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, reference):
        """Load the given reference

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def unload(self, reference):
        """Unload the given reference

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, reference, taskfileinfo):
        """Replace the given reference with the given taskfileinfo

        :param reference: the reference object. E.g. in Maya a reference node
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, refobj):
        """Delete the content of the given refobj

        :param refobj: the refobj that represents the content that should be deleted
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def import_reference(self, reference):
        """Import the given reference

        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def import_taskfile(self, refobj, taskfileinfo):
        """Import the given taskfileinfo and update the refobj

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_replaceable(self, refobj):
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_options(self, element):
        """Fetch the options for possible files to
        load replace etc for the given element.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: the options
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        raise NotImplementedError
