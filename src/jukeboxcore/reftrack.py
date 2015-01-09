"""This module features classes and interfaces to track references and loaded data and manipulate it.

Overview
------------

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

Entity Types
------------

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

Parents
-------

Each :class:`Reftrack` object can have a parent. A parent is another :class:`Reftack` object and is responsible
for its children. If the parent is deleted, all other children should be deleted too. This might be the case for a shader.
Imagine assigning a shader to an asset. The asset would be the parent and the shader the child. If the asset gets deleted
the shader should be deleted to. The :class:`Reftrack` objects handle such cases by themselves.

Root
----

There is also a :class:`ReftrackRoot` class. It is important to group all reftracks of your current scene under the same root.
The root object is mainly used to find parent :class:`Reftrack` objects. But it also provides a Qt model that you can use
for views. It holds all :class:`Reftrack` objects in a tree model.

Creating a Reftrack
-------------------

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

Restrictions
------------

You can restrict certain actions on a :class:`Reftrack` instance. All methods that have the decorator :func:`restrictable` can be
restricted by using :meth:`Reftrack.set_restricted`. Usually this is automatically done. E.g. you cannot replace an entity if it is not
already in the scene. In this case a :class:`ReftrackIntegrityError` would be raised by the decorated method automatically.
See: :meth:`Reftrack.fetch_reference_restriction`, :meth:`Reftrack.fetch_load_restriction`, :meth:`Reftrack.fetch_unload_restriction`,
:meth:`Reftrack.fetch_import_ref_restriction`, :meth:`Reftrack.fetch_import_f_restriction`, :meth:`Reftrack.fetch_replace_restriction`.

The :class:`RefobjInterface` or :class:`ReftypeInterface` can customize the rules for restrictions.
For example you could create a rule, that nested references in Maya cannot be replaced.

Usage
-----

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
    # alternatively if you only want to wrap the ones you haven't
    # this would return all refobjects that are not in root
    newrefobjs = Reftrack.get_unwrapped(reftrackroot, refobjinter)
    newreftracks = Reftrack.wrap(reftrackroot, refobjinter, newrefobjs)
    # convenience function to wrap unwrapped refobjects and also get suggestions:
    newrefobjs = Reftrack.wrap_scene(reftrackroot, refobjinter)

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

  You could also simply get a list of the avaliable :class:`TaskFileInfo` of the options
  by using::

    # get all options
    options = reftrack.get_option_taskfileinfos()
    # assert that there are any available options
    if options:
        # pick one
        reftrack.import_entity(options[0])

Get Started
-----------

So before you start, here is a list of things to do:

  1. Implement a :class:`ReftypeInterface` for each type.
  2. Implement :class:`RefobjInterface`. Make sure it has
     all the types registered. See :meth:`RefobjInterface.register_type`.
  3. Think about creating your custom :class:`jukeboxcore.gui.treemodel.ItemData`
     for :class:`Reftrack` objects.
  4. Create a :class:`RefobjInterface` instance.
  5. Create a :class:`ReftrackRoot` instance.
  6. For refobjs in your scene use :meth:`Reftrack.wrap` or :meth:`Reftrack.wrap_scene`.
  7. Add new reftracks.

"""
import abc
import functools
from contextlib import contextmanager

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.treemodel import TreeModel, TreeItem, ListItemData
from jukeboxcore.gui.reftrackitemdata import ReftrackItemData
from jukeboxcore.errors import ReftrackIntegrityError
from jukeboxcore import djadapter


class ReftrackRoot(object):
    """Groups a collection of :class:`Reftrack` objects.

    Enables the search for parents via the refobject.
    Provides a :class:`jukeboxcore.gui.treemodel.TreeModel` that can be used
    in views, to display all reftracks.

    The model that is created and also updated uses the root item and itemdata class
    you provided in the constructor. The root item is used for headers in your views.
    So you could create a root item like this::

      rootdata = ListItemData(["Name", "Status", "Version"])  # root data will be used for headers in views
      rootitem = TreeItem(rootdata)

    The itemdata class will be used to provide data for the model about :class:`Reftrack` object.
    You can provide your own subclass or omit the rootitem and itemdataclass. Then a default
    root item and itemdata class will be used.

    """
    def __init__(self, rootitem=None, itemdataclass=None):
        """Initialize a new Reftrack root with a given root tree item and
        a :class:`jukeboxcore.gui.treemodel.ItemData` class to wrap
        the :class:`Reftrack` objects.

        The ItemData class should accept a :class:`Reftrack` object as
        first argument in the constructor.

        :param rootitem: the root tree item for the treemodel.
                         The root tree item will be responsible for the headers in a view.
                         If no rootitem is provided, a default one is used.
        :type rootitem: :class:`jukeboxcore.gui.treemodel.TreeItem` | None
        :param itemdataclass: the itemdata subclass to be used for wrapping the :class:`Reftrack` objects
                              in the model. Not an instance! A class! The constructor should accept
                              a :class:`Reftrack` object as first argument.
                              If no class is provided, a default one is used. See: :class:`ReftrackItemData`
        :type itemdataclass: :class:`jukeboxcore.gui.treemodel.ItemData` | None
        :raises: None
        """
        if rootitem is None:
            rootdata = ListItemData(["Type",
                                     "Seq/Atype",
                                     "Shot/Asset",
                                     "Task",
                                     "Releasetype",
                                     "Descriptor",
                                     "Version",
                                     "Status",
                                     "Uptodate",
                                     "Alien",
                                     "Path",
                                     "Referencing Restricted",
                                     "Loading Restricted",
                                     "Unloading Restricted",
                                     "Import Reference Restricted",
                                     "Import File Restricted",
                                     "Replace Restricted",
                                     "Identifier",
                                     "Reftrack Object"])
            rootitem = TreeItem(rootdata)
        if itemdataclass is None:
            itemdataclass = ReftrackItemData

        self._model = TreeModel(rootitem)
        self._rootitem = rootitem
        self._idataclass = itemdataclass
        self._reftracks = set()  # a list of all reftracks in belonging to the root
        self._parentsearchdict = {}
        """Keys are the refobjs of the Reftrack and the values are the Reftrack objects.
        So you can easily find the parent Reftrack for a parent refobj."""

    def get_model(self, ):
        """Return the treemodel that contains all reftracks of this root

        The model uses the provided :class:`jukeboxcore.gui.treem.ItemData`.
        The model is automatically updated.

        :returns: The treemodel
        :rtype: :class:`TreeModel`
        :raises: None
        """
        return self._model

    def get_rootitem(self, ):
        """Return the rootitem of the treemodel

        The root item is responsible for the headers.
        When adding new TreeItems to the root level use this
        item as parent.

        :returns: the rootitem
        :rtype: :class:`TreeItem`
        :raises: None
        """
        return self._rootitem

    def add_reftrack(self, reftrack):
        """Add a reftrack object to the root.

        This will not handle row insertion in the model!
        It is automatically done when setting the parent of the :class:`Reftrack` object.

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
        It is automatically done when calling :meth:`Reftrack.delete`.

        :param reftrack: the reftrack object to remove
        :type reftrack: :class:`Reftrack`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._reftracks.remove(reftrack)
        refobj = reftrack.get_refobj()
        if refobj and refobj in self._parentsearchdict:
            del self._parentsearchdict[refobj]

    def update_refobj(self, old, new, reftrack):
        """Update the parent search dict so that the reftrack can be found
        with the new refobj and delete the entry for the old refobj.

        Old or new can also be None.

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
        :type refobj: refobj | None
        :returns: The reftrack instance that wraps the given refobj.
                  If no instance is found in this root, a KeyError is raised.
                  If None was given, None is returned
        :rtype: :class:`Reftrack` | None
        :raises: :class:`KeyError`
        """
        if refobj is None:
            return None
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

    def get_scene_suggestions(self, refobjinter):
        """Return a list of suggested Reftracks for the current scene, that are not already
        in this root.

        A suggestion is a combination of type and element.

        :param refobjinter: a programm specific reftrack object interface
        :type refobjinter: :class:`RefobjInterface`
        :returns: A list of suggestions
        :rtype: :class:`list`
        :raises: None
        """
        sugs = []
        cur = refobjinter.get_current_element()
        if not cur:
            return sugs
        for typ in refobjinter.types:
            inter = refobjinter.get_typ_interface(typ)
            elements = inter.get_scene_suggestions(cur)
            for e in elements:
                for r in self._reftracks:
                    if not r.get_parent() and typ == r.get_typ() and e == r.get_element():
                        break
                else:
                    sugs.append((typ, e))
        return sugs


def restrictable(m):
    """Decorator for :class:`Reftrack` methods.
    A decorated method will check if its restriction with :meth:`Reftrack.is_restricted`
    and raises a :class:`RestrictionError` if it is restricted.

    :param m: The :class:`Reftrack` method to wrap
    :type m: :class:`Reftrack` method
    :returns: a wrapped method
    :rtype: method
    :raises: None
    """
    @functools.wraps(m)
    def wrapper(*args, **kwds):
        self = args[0]
        if wrapper in self._restricted:
            msg = "Method: %s restricted on %s" % (m.__name__, self)
            raise ReftrackIntegrityError(msg=msg, reftracks=[self])
        return m(*args, **kwds)
    return wrapper


class Reftrack(object):
    """Represents one entity of the reference workflow in a programm

    Stores information like the status, options for replacing the entity etc.
    Delegates actions to the appropriate interfaces.
    So no matter what kind of programm you are in and what type your entity is, the :class:`Reftrack` object
    can carry out all actions as long as you provide 2 interfaces.

    A refobj interface will interact will query information about the entity and can create
    a new refobj, which will store the information in the scene. E.g. in Maya it might be a node
    which has a connection to the reference node, stores the type of the entity etc.
    The refobj interface is responsible for creating, editing, deleting the refobj.
    The refobj interface can query the reftrack object which element the entity represents (which Shot or Asset).

    The typ interface is programm and type specific. It manipulates the actual content of the entity.
    E.g. it will assign shaders upon loading, create references, connect nodes or group the referenced
    objects.

    The :class:`Reftrack` object only interacts with the :class:`RefobjInterface`. The interface will interact
    with the appropriate :class:`ReftypeInterface`. So whatever type your :class:`Reftrack` object will be,
    make sure, your :class:`RefobjInterface` supports it.

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
                     later, because the parent cannot be changed. Only if the parent was None it is possible.
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
        :raises: TypeError, ValueError
        """
        if not (refobj or (typ and element)):
            raise TypeError("Please provide either a refobj or a typ and element.")
        if refobj and (parent or typ or element):
            raise TypeError("Refobject given. Providing a typ, element or parent is invalid. \
The Refobject provides the necessary info.")
        self._root = root
        self._refobjinter = refobjinter
        self._refobj = refobj
        self._taskfileinfo = None  # the taskfileinfo that the refobj represents
        self._typ = None
        self._typicon = None
        self._element = None
        self._parent = None
        self._children = []
        self._options = None  # tree model of possible files to load
        self._taskfileinfo_options = []  # list of taskfileinfos that are in options
        self._uptodate = None
        self._alien = True
        self._status = None
        self._restricted = set([])  # restrict actions
        self._id = -1  # ID is just for the user/interface to sort reftracks of the same element, type and parent
        self._treeitem = self.create_treeitem()  # a treeitem for the model of the root
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
            self._id = refobjinter.get_id(self._refobj)

        self._root.add_reftrack(self)
        self.update_restrictions()
        self.emit_data_changed()

    @classmethod
    def wrap(cls, root, refobjinter, refobjects):
        """Wrap the given refobjects in a :class:`Reftrack` instance
        and set the right parents

        This is the preferred method for creating refobjects. Because you cannot set
        the parent of a :class:`Reftrack` before the parent has been wrapped itselfed.

        :param root: the root that groups all reftracks and makes it possible to search for parents
        :type root: :class:`ReftrackRoot`
        :param refobjinter: a programm specific reftrack object interface
        :type refobjinter: :class:`RefobjInterface`
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
            if parentrefobj:
                parentreftrack = root.get_reftrack(parentrefobj)
            else:
                parentreftrack = None
            t.set_parent(parentreftrack)
            t.fetch_new_children()
            t.update_restrictions()
            t.emit_data_changed()
        return tracks

    @classmethod
    def wrap_scene(cls, root, refobjinter):
        """Wrap all refobjects in the scene in a :class:`Reftrack` instance
        and set the right parents, also add suggestions for the current scene

        When you want to quickly scan the scene and display the reftracks in a tool,
        this is the easiest function.

        It uses wrap on all refobjects in the scene, then adds suggestions for the
        current scene.

        :param root: the root that groups all reftracks and makes it possible to search for parents
        :type root: :class:`ReftrackRoot`
        :param refobjinter: a programm specific reftrack object interface
        :type refobjinter: :class:`RefobjInterface`
        :returns: list with the wrapped :class:`Reftrack` instances
        :rtype: list
        :raises: None
        """
        refobjects = cls.get_unwrapped(root, refobjinter)
        tracks = cls.wrap(root, refobjinter, refobjects)
        sugs = root.get_scene_suggestions(refobjinter)
        for typ, element in sugs:
            r = cls(root=root, refobjinter=refobjinter, typ=typ, element=element)
            tracks.append(r)
        return tracks

    @classmethod
    def get_unwrapped(self, root, refobjinter):
        """Return a set with all refobjects in the scene that are not in already
        wrapped in root.

        :param root: the root that groups all reftracks and makes it possible to search for parents
        :type root: :class:`ReftrackRoot`
        :param refobjinter: a programm specific reftrack object interface
        :type refobjinter: :class:`RefobjInterface`
        :returns: a set with unwrapped refobjects
        :rtype: set
        :raises: None
        """
        all_refobjs = set(refobjinter.get_all_refobjs())
        wrapped = set(root._parentsearchdict.keys())
        return all_refobjs - wrapped

    def get_root(self, ):
        """Return the ReftrackRoot this instance belongs to.

        :returns: the root
        :rtype: :class:`ReftrackRoot`
        :raises: None
        """
        return self._root

    def get_refobj(self, ):
        """Return the reftrack object, the physical representation of your :class:`Reftrack` object in the scene.
        If the entity is not loaded, None is returned.

        :returns: the reftrack object
        :rtype: None | reftrack object
        :raises: None
        """
        return self._refobj

    def set_refobj(self, refobj, setParent=True):
        """Set the reftrack object.

        The reftrack object interface will determine typ, element, taskfileinfo, status and parent and set these values.
        If the reftrack object is None, the :class:`Reftrack` object will keep the initial typ,
        element but will loose it\'s parent, status and taskfileinfo

        :param refobj: a reftrack object or None
        :type refobj: None | reftrack object
        :param setParent: If True, set also the parent
        :type setParent: :class:`bool`
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
            if setParent:
                parentrefobj = refobjinter.get_parent(self._refobj)
                parentreftrack = root.get_reftrack(parentrefobj)
                self.set_parent(parentreftrack)
            self.set_status(refobjinter.get_status(self._refobj))
        else:
            self.set_taskfileinfo(None)
            if setParent:
                self.set_parent(None)
            self.set_status(None)
        root.update_refobj(old, refobj, self)
        self.fetch_uptodate()

    def get_typ(self, ):
        """Return the type of the entity

        E.g. Asset, Alembic, Camera etc.
        The type will also be a key in :data:`RefobjInterface.types`.

        :returns: the type of the entity
        :rtype: str
        :raises: None
        """
        return self._typ

    def set_typ(self, typ):
        """Set the type of the entity

        Make sure the type is registered in the :class:`RefobjInterface`.

        :param typ: the type of the entity
        :type typ: str
        :returns: None
        :rtype: None
        :raises: ValueError
        """
        if typ not in self._refobjinter.types:
            raise ValueError("The given typ is not supported by RefobjInterface. Given %s, supported: %s" %
                             (typ, self._refobjinter.types.keys()))
        self._typ = typ
        self._typicon = self.get_refobjinter().get_typ_icon(typ)

    def get_typ_icon(self, ):
        """Return the icon for the type

        :returns: the icon that should be used in UIs to identify the type
        :rtype: :class:`QtGui.QIcon` | None
        :raises: None
        """
        return self._typicon

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
        or referencing. See :meth:`Reftrack.get_options` and :meth:`Reftrack.fetch_options`.
        The :class:`ReftypeInterface.fetch_options` is responsible for providing a treemodel
        with :class:`jukeboxcore.gui.treemodel.TaskFileInfo` as leaves.

        So if the element is be a character asset and the type is "Shader", only the shading handoff
        files for this asset would be considered.

        :returns: The element the reftrack represents
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        return self._element

    def set_element(self, element):
        """Set the element for the reftrack to represent.

        The element is either an Asset or a Shot.
        Depending on the type only certain files are considered for loading
        or referencing. See :meth:`Reftrack.get_options` and :meth:`Reftrack.fetch_options`.
        The :class:`ReftypeInterface.fetch_options` is responsible for providing a treemodel
        with :class:`jukeboxcore.gui.treemodel.TaskFileInfo` as leaves.

        So if the element is be a character asset and the type is "Shader", only the shading handoff
        files for this asset would be considered.

        This will also set the available options and set the alien status.

        :param element: The element the reftrack represents.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._element = element
        self.fetch_options()

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
        assert self._parent is None or self._parent is parent,\
            "Cannot change the parent. Can only set from None."
        if parent and self._parent is parent:
            return
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
        if not self.get_refobj():
            self.set_id(self.fetch_new_id())

        pitem = self._parent._treeitem if self._parent else self.get_root().get_rootitem()
        self._treeitem.set_parent(pitem)
        self.fetch_alien()

    def get_id(self, ):
        """Return the id of the reftrack

        An id is a integer number that will be unique between
        all reftracks of the same parent, element and type, that have a
        refobject

        :returns: the id
        :rtype: int
        :raises: None
        """
        return self._id

    def set_id(self, identifier):
        """Set the id of the given reftrack

        This will set the id on the refobject

        :param identifier: the identifier number
        :type identifier: int
        :returns: None
        :rtype: None
        :raises: None
        """
        self._id = identifier
        refobj = self.get_refobj()
        if refobj:
            self.get_refobjinter().set_id(refobj, identifier)

    def fetch_new_id(self, ):
        """Return a new id for the given reftrack to be set on the refobject

        The id can identify reftracks that share the same parent, type and element.

        :returns: A new id
        :rtype: int
        :raises: None
        """
        parent = self.get_parent()
        if parent:
            others = parent._children
        else:
            others = [r for r in self.get_root()._reftracks if r.get_parent() is None]
        others = [r for r in others
                  if r != self
                  and r.get_typ() == self.get_typ()
                  and r.get_element() == self.get_element()]
        highest = -1
        for r in others:
            identifier = r.get_id()
            if identifier > highest:
                highest = identifier
        return highest + 1

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
        else:
            pitem = root.get_rootitem()
        idata = root.create_itemdata(self)
        item = TreeItem(idata, parent=pitem)
        return item

    def get_treeitem(self, ):
        """Return the treeitem that wraps this instance.

        There is only a treeitem if the parent has been set once.
        If you use :meth:`Reftrack.wrap` or initialize a new Reftrack
        object with type and element, it will have one.
        Only if you initialize a new Reftrack with a given refobj,
        :meth:`Reftrack.set_parent` will not be called automatically.

        :returns: the treeitem for this instance
        :rtype: :class:`TreeItem` | None
        :raises: None
        """
        return self._treeitem

    def add_child(self, reftrack):
        """Add the given reftrack object as child

        .. Note:: Does not set the parent of the child!
                  Use :meth:`Reftrack.set_parent` instead.

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
                  Use :meth:`Reftrack.delete` instead.

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
        self._options, self._taskfileinfo_options = self.get_refobjinter().fetch_options(self.get_typ(), self.get_element())
        return self._options

    def get_option_taskfileinfos(self, ):
        """Return a list of all :class:`TaskFileInfo` that are available as options for
        referencing, importing, replacing etc.

        :returns: list of TaskFileInfos
        :rtype: :class:`TaskFileInfo`
        :raises: None
        """
        return self._taskfileinfo_options

    def get_option_labels(self,):
        """Return labels for each level of the option model.

        The options returned by :meth:`Reftrack.fetch_options` is a treemodel
        with ``n`` levels. Each level should get a label to describe what is displays.

        E.g. if you organize your options, so that the first level shows the tasks, the second
        level shows the descriptors and the third one shows the versions, then
        your labels should be: ``["Task", "Descriptor", "Version"]``.

        :returns: label strings for all levels
        :rtype: list
        :raises: None
        """
        return self.get_refobjinter().get_option_labels(self.get_typ(), self.get_element())

    def get_option_columns(self):
        """Return the column of the model to show for each level

        Because each level might be displayed in a combobox. So you might want to provide the column
        to show.

        :returns: a list of columns
        :rtype: list
        :raises: None
        """
        return self.get_refobjinter().get_option_columns(self.get_typ(), self.get_element())

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
            self._uptodate = tfi.is_latest()
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
        parent = self.get_parent()
        if parent:
            parentelement = parent.get_element()
        else:
            parentelement = self.get_refobjinter().get_current_element()
            if not parentelement:
                self._alien = True
                return self._alien
        element = self.get_element()
        if element == parentelement:
            self._alien = False
        # test if it is the element is a global shot
        # first test if we have a shot
        # then test if it is in a global sequence. then the shot is global too.
        # test if the parent element is a shot, if they share the sequence, and element is global
        elif isinstance(element, djadapter.models.Shot)\
            and (element.sequence.name == djadapter.GLOBAL_NAME\
            or (isinstance(parentelement, djadapter.models.Shot)\
                and parentelement.sequence == element.sequence and element.name == djadapter.GLOBAL_NAME)):
            self._alien = False
        else:
            assets = parentelement.assets.all()
            self._alien = element not in assets
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
        """Create a refobject in the scene that represents the :class:`Reftrack` instance.

        .. Note:: This will not set the reftrack object.

        :returns: the created reftrack object
        :rtype: scene object
        :raises: None
        """
        parent = self.get_parent()
        if parent:
            prefobj = parent.get_refobj()
        else:
            prefobj = None
        refobj = self.get_refobjinter().create(self.get_typ(), self.get_id(), prefobj)
        return refobj

    @restrictable
    def reference(self, taskfileinfo):
        """Reference the entity into the scene. Only possible if the current status is None.

        This will create a new refobject, then call :meth:`RefobjInterface.reference` and
        afterwards set the refobj on the :class:`Reftrack` instance.

        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: :class:`ReftrackIntegrityError`
        """
        assert self.status() is None,\
            "Can only reference, if the entity is not already referenced/imported. Use replace instead."
        refobj = self.create_refobject()
        with self.set_parent_on_new(refobj):
            self.get_refobjinter().reference(taskfileinfo, refobj)
        self.set_refobj(refobj)
        self.fetch_new_children()
        self.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def load(self, ):
        """If the reference is in the scene but unloaded, load it.

        .. Note:: Do not confuse this with reference or import. Load means that it is already referenced.
                  But the data from the reference was not read until now. Load loads the data from the reference.

        This will call :meth:`RefobjInterface.load` and set the status to :data:`Reftrack.LOADED`.

        :returns: None
        :rtype: None
        :raises: :class:`ReftrackIntegrityError`
        """
        assert self.status() == self.UNLOADED,\
            "Cannot load if there is no unloaded reference. Use reference instead."
        self.get_refobjinter().load(self._refobj)
        self.set_status(self.LOADED)
        self.fetch_new_children()
        self.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def unload(self, ):
        """If the reference is loaded, unload it.

        .. Note:: Do not confuse this with a delete. This means, that the reference stays in the
                  scene, but no data is read from the reference.

        This will call :meth:`RefobjInterface.unload` and set the status to :data:`Reftrack.UNLOADED`.
        It will also throw away all children :class:`Reftrack`. They will return after :meth:`Reftrack.load`.

        The problem might be that children depend on their parent, but will not get unloaded.
        E.g. you imported a child. It will stay in the scene after the unload and become an orphan.
        In this case an error is raised. It is not possible to unload such an entity.
        The orphan might get its parents back after you call load, but it will introduce bugs when
        wrapping children of unloaded entities. So we simply disable the feature in that case and raise
        an :class:`IntegrityError`

        :returns: None
        :rtype: None
        :raises: :class:`ReftrackIntegrityError`
        """
        assert self.status() == self.LOADED,\
            "Cannot unload if there is no loaded reference. \
Use delete if you want to get rid of a reference or import."
        childrentodelete = self.get_children_to_delete()
        if childrentodelete:
            raise ReftrackIntegrityError("Cannot unload because children of the reference would become orphans.", childrentodelete)
        self.get_refobjinter().unload(self._refobj)
        self.set_status(self.UNLOADED)
        self.throw_children_away()
        self.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def import_file(self, taskfileinfo):
        """Import the file for the given taskfileinfo

        This will also update the status to :data:`Reftrack.IMPORTED`. This will also call
        :meth:`fetch_new_children`. Because after the import, we might have new children.

        :param taskfileinfo: the taskfileinfo to import. If None is given, try to import
                             the current reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: :class:`ReftrackIntegrityError`
        """
        assert self.status() is None,\
            "Entity is already in scene. Use replace instead."
        refobjinter = self.get_refobjinter()
        refobj = self.create_refobject()
        with self.set_parent_on_new(refobj):
            refobjinter.import_taskfile(refobj, taskfileinfo)
        self.set_refobj(refobj)
        self.set_status(self.IMPORTED)
        self.fetch_new_children()
        self.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def import_reference(self, ):
        """Import the currently loaded reference

        This will also update the status to :data:`Reftrack.IMPORTED`.

        :returns: None
        :rtype: None
        :raises: :class:`ReftrackIntegrityError`
        """
        assert self.status() in (self.LOADED, self.UNLOADED),\
            "There is no reference for this entity."
        refobjinter = self.get_refobjinter()
        refobjinter.import_reference(self.get_refobj())
        self.set_status(self.IMPORTED)
        self.update_restrictions()
        for c in self.get_all_children():
            c.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def replace(self, taskfileinfo):
        """Replace the current reference or imported entity.

        If the given refobj is not replaceable, e.g. it might be imported
        or it is not possible to switch the data, then the entity will be deleted,
        then referenced or imported again, depending on the current status.

        A replaced entity might have other children. This introduces a problem:

          A child might get deleted, e.g. an asset which itself has another child,
          that will not get deleted, e.g. an imported shader. In this case the imported
          shader will be left as an orphan.
          This will check all children that will not be deleted (:meth:`Reftrack.get_children_to_delete`)
          and checks if they are orphans after the replace. If they are, they will get deleted!

        After the replace, all children will be reset. This will simply throw away all children reftracks
        (the content will not be deleted) and wrap all new children again. See: :meth:`Reftrack.fetch_new_children`.

        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: ReftrackIntegrityError
        """
        assert self.status() is not None,\
            "Can only replace entities that are already in the scene."
        refobjinter = self.get_refobjinter()
        refobj = self.get_refobj()
        if self.status() in (self.LOADED, self.UNLOADED) and refobjinter.is_replaceable(refobj):
            # possible orphans will not get replaced, by replace
            # but their parent might dissapear in the process
            possibleorphans = self.get_children_to_delete()
            with self.set_parent_on_new(refobj):
                refobjinter.replace(refobj, taskfileinfo)
            self.set_taskfileinfo(taskfileinfo)
            self.fetch_uptodate()
            for o in possibleorphans:
                # find if orphans were created and delete them
                # we get the refobj of the parent
                # if it still exists, it is no orphan
                parent = o.get_parent()
                refobj = parent.get_refobj()
                if not parent.get_refobjinter().exists(refobj):
                    # orphans will be deleted!
                    # this is politically incorrect, i know!
                    # the world of programming is a harsh place.
                    o.delete()
            # reset the children
            # throw them away at first
            self.throw_children_away()
            # gather them again
            self.fetch_new_children()
        else:
            status = self.status()
            self.delete(removealien=False)
            if status == self.IMPORTED:
                self.import_file(taskfileinfo)
            else:
                self.reference(taskfileinfo)
        self.update_restrictions()
        self.emit_data_changed()

    @restrictable
    def delete(self, removealien=True):
        """Delete the current entity.

        This will also call :meth:`RefobjInterface.get_children_to_delete` and
        delete these children first by calling :meth:`Reftrack.delete`.
        To delete the content it will call :meth:`RefobjInterface.delete`.
        Then the refobject will be set to None. If the :class:`Reftrack` object is an alien to
        the current scene, because it is not linked in the database, it will also remove itself
        from the root and from the treemodel.
        If it is not an alien, it will just empty all of tis children and update its status.

        :param removealien: If True, remove this reftrack, if it is an alien
        :type removealien: :class:`bool`
        :returns: None
        :rtype: None
        :raises: None
        """
        if self.status() is None:
            parent = self.get_parent()
            if parent:
                parent.remove_child(self)
            self._treeitem.parent().remove_child(self._treeitem)
            self.get_root().remove_reftrack(self)
            return
        todelete = self.get_children_to_delete()
        allchildren = self.get_all_children()
        for c in reversed(todelete):
            c._delete()
        for c in allchildren:
            self.get_root().remove_reftrack(c)
        self._delete()
        if self.alien() and removealien:
            self.get_root().remove_reftrack(self)
        self.update_restrictions()
        self.emit_data_changed()

    def _delete(self, ):
        """Internal implementation for deleting a reftrack.

        This will just delete the reftrack, set the children to None,
        update the status, and the rootobject. If the object is an alien,
        it will also set the parent to None, so it dissapears from the model.

        :returns: None
        :rtype: None
        :raises: None
        """
        refobjinter = self.get_refobjinter()
        refobjinter.delete(self.get_refobj())
        self.set_refobj(None, setParent=False)
        if self.alien():
            # it should not be in the scene
            # so also remove it from the model
            # so we cannot load it again
            parent = self.get_parent()
            if parent:
                parent.remove_child(self)
            self._treeitem.parent().remove_child(self._treeitem)
        else:
            # only remove all children from the model and set their parent to None
            for c in self.get_all_children():
                c._parent = None
                self._treeitem.remove_child(c._treeitem)
        # this should not have any children anymore
        self._children = []
        self.set_status(None)

    def duplicate(self, ):
        """Return a new :class:`Reftrack` instance that has the same
        typ, element and parent. The new reference will be not referenced or imported!

        :returns: a new reftrack instance with same typ, element and parent
        :rtype: :class:`Reftrack`
        :raises: None
        """
        return self.__class__(root=self.get_root(),
                              refobjinter=self.get_refobjinter(),
                              typ=self.get_typ(),
                              element=self.get_element(),
                              parent=self.get_parent())

    def get_all_children(self):
        """Get all children including children of children

        :returns: all children including children of children
        :rtype: list of :class:`Reftrack`
        :raises: None
        """
        children = self._children[:]
        oldlen = 0
        newlen = len(children)
        while oldlen != newlen:
            start = oldlen
            oldlen = len(children)
            for i in range(start, len(children)):
                children.extend(children[i]._children)
            newlen = len(children)
        return children

    def get_children_to_delete(self):
        """Return all children that are not referenced

        :returns: list or :class:`Reftrack`
        :rtype: list
        :raises: None
        """
        refobjinter = self.get_refobjinter()
        children = self.get_all_children()

        todelete = []
        for c in children:
            if c.status() is None:
                # if child is not in scene we do not have to delete it
                continue
            rby = refobjinter.referenced_by(c.get_refobj())
            if rby is None:
                # child is not part of another reference.
                # we have to delete it for sure
                todelete.append(c)
                continue
            # check if child is referenced by any parent up to self
            # if it is not referenced by any refrence of a parent, then we
            # can assume it is referenced by a parent of a greater scope,
            # e.g. the parent of self. because we do not delete anything above self
            # we would have to delete the child manually
            parent = c.get_parent()
            while parent != self.get_parent():
                if refobjinter.get_reference(parent.get_refobj()) == rby:
                    # is referenced by a parent so it will get delted when the parent is deleted.
                    break
                parent = parent.get_parent()
            else:
                todelete.append(c)
        return todelete

    def get_suggestions(self, ):
        """Return a list with possible children for this reftrack

        Each Reftrack may want different children. E.g. a Asset wants
        to suggest a shader for itself and all assets that are linked in
        to it in the database. Suggestions only apply for enities with status
        other than None.

        A suggestion is a tuple of typ and element. It will be used to create a newlen
        :class:`Reftrack`. The parent will be this instance, root and interface will
        of course be the same.

        This will call :meth:`RefobjInterface.get_suggestions` which will delegate the call to the
        appropriate :class:`ReftypeInterface`. So suggestions may vary for every typ and might depend on the
        status of the reftrack.

        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: None
        """
        return self.get_refobjinter().get_suggestions(self)

    def fetch_new_children(self, ):
        """Collect all new children and add the suggestions to the children as well

        When an entity is loaded, referenced, imported etc there might be new children.
        Also it might want to suggest children itself, like a Shader for an asset.

        First we wrap all unwrapped children. See: :meth:`Reftrack.get_unwrapped`, :meth:`Reftrack.wrap`.
        Then we get the suggestions. See: :meth:`Reftrack.get_suggestions`. All suggestions that are not
        already a child of this Reftrack instance, will be used to create a new Reftrack with the type
        and element of the suggestion and the this instance as parent.

        :returns: None
        :rtype: None
        :raises: None
        """
        root = self.get_root()
        refobjinter = self.get_refobjinter()
        unwrapped = self.get_unwrapped(root, refobjinter)
        self.wrap(self.get_root(), self.get_refobjinter(), unwrapped)

        suggestions = self.get_suggestions()
        for typ, element in suggestions:
            for c in self._children:
                if typ == c.get_typ() and element == c.get_element():
                    break
            else:
                Reftrack(root=root, refobjinter=refobjinter, typ=typ, element=element, parent=self)

    def throw_children_away(self, ):
        """Get rid of the children :class:`Reftrack` by deleting them from root,
        and unparenting them. The content of the children will stay in the scene.

        You can wrap them again. It is a simple way to reset all children, e.g. after
        a replace. Because they might have changed completly.

        :returns: None
        :rtype: None
        :raises: None
        """
        for c in self._children:
            c._parent = None
            self._treeitem.remove_child(c._treeitem)
        for c in self.get_all_children():
            self.get_root().remove_reftrack(c)
        self._children = []

    @contextmanager
    def set_parent_on_new(self, parentrefobj):
        """Contextmanager that on close will get all new
        unwrapped refobjects, and for every refobject with no parent
        sets is to the given one.

        :returns: None
        :rtype: None
        :raises: None
        """
        refobjinter = self.get_refobjinter()
        # to make sure we only get the new one
        # we get all current unwrapped first
        old = self.get_unwrapped(self.get_root(), refobjinter)
        yield
        new = self.get_unwrapped(self.get_root(), refobjinter) - old
        for refobj in new:
            if refobjinter.get_parent(refobj) is None:
                refobjinter.set_parent(refobj, parentrefobj)

    def is_restricted(self, obj):
        """Returns True if the given object is listed under :data:`Reftrack.restricted`.

        This is mainly used to restrict functions in certain situations.

        :param obj: a hashable object
        :returns: True, if the given obj is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return obj in self._restricted

    def set_restricted(self, obj, restricted):
        """Set the restriction on the given object.

        You can use this to signal that a certain function is restricted.
        Then you can query the restriction later with :meth:`Reftrack.is_restricted`.

        :param obj: a hashable object
        :param restricted: True, if you want to restrict the object.
        :type restricted: :class:`bool`
        :returns: None
        :rtype: None
        :raises: None
        """
        if restricted:
            self._restricted.add(obj)
        elif obj in self._restricted:
            self._restricted.remove(obj)

    def update_restrictions(self, ):
        """Update all restrictions for the common :class:`Reftrack` actions.

        Update restrictions for:

          * :meth:`Reftrack.reference`
          * :meth:`Reftrack.load`
          * :meth:`Reftrack.unload`
          * :meth:`Reftrack.import_reference`
          * :meth:`Reftrack.import_file`
          * :meth:`Reftrack.replace`

        :returns: None
        :rtype: None
        :raises: None
        """
        self.set_restricted(self.reference, self.fetch_reference_restriction())
        self.set_restricted(self.load, self.fetch_load_restriction())
        self.set_restricted(self.unload, self.fetch_unload_restriction())
        self.set_restricted(self.import_reference, self.fetch_import_ref_restriction())
        self.set_restricted(self.import_file, self.fetch_import_f_restriction())
        self.set_restricted(self.replace, self.fetch_replace_restriction())
        self.set_restricted(self.delete, self.fetch_delete_restriction())

    def fetch_reference_restriction(self, ):
        """Fetch whether referencing is restricted

        :returns: True, if referencing is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() is not None
        return restricted or inter.fetch_action_restriction(self, 'reference')

    def fetch_load_restriction(self, ):
        """Fetch whether loading is restricted

        :returns: True, if loading is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() != self.UNLOADED
        return restricted or inter.fetch_action_restriction(self, 'load')

    def fetch_unload_restriction(self, ):
        """Fetch whether unloading is restricted

        :returns: True, if unloading is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() != self.LOADED or self.get_children_to_delete()
        return restricted or inter.fetch_action_restriction(self, 'unload')

    def fetch_import_ref_restriction(self,):
        """Fetch whether importing the reference is restricted

        :returns: True, if importing the reference is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() not in (self.LOADED, self.UNLOADED)
        return restricted or inter.fetch_action_restriction(self, 'import_reference')

    def fetch_import_f_restriction(self,):
        """Fetch whether importing a file is restricted

        :returns: True, if import is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() is not None
        return restricted or inter.fetch_action_restriction(self, 'import_taskfile')

    def fetch_replace_restriction(self, ):
        """Fetch whether unloading is restricted

        :returns: True, if unloading is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        restricted = self.status() is None
        return restricted or inter.fetch_action_restriction(self, 'replace')

    def fetch_delete_restriction(self, ):
        """Fetch whether deletion is restricted

        :returns: True, if deletion is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_refobjinter()
        return inter.fetch_action_restriction(self, 'delete')

    def emit_data_changed(self):
        """Emit the data changed signal on the model of the treeitem
        if the treeitem has a model.

        :returns: None
        :rtype: None
        :raises: None
        """
        item = self.get_treeitem()
        m = item.get_model()
        if m:
            start = m.index_of_item(item)
            parent = start.parent()
            end = m.index(start.row(), item.column_count()-1, parent)
            m.dataChanged.emit(start, end)

    def get_additional_actions(self,):
        """Return a list of additional actions you want to provide for the menu
        of the reftrack.

        E.e. you want to have a menu entry, that will select the entity in your programm.

        This will call :meth:`RefobjInterface.get_additional_actions`.

        The base implementation returns an empty list.

        :returns: A list of :class:`ReftrackAction`
        :rtype: list
        :raises: None
        """
        if self.get_typ():
            inter = self.get_refobjinter()
            return inter.get_additional_actions(self)
        else:
            return []


class RefobjInterface(object):
    """Interface to interact with a refernece object that is in your scene.

    This interface is abstract. You should implement it for every software where you need
    a reference workflow.
    To interact with the content of each entity, there is a special reftyp interface that
    is not only software specific but also handles only a certain type of entity.
    You can register additional type interfaces, so plugins can introduce their own entity types.
    See :data:`RefobjInterface.types`. When subclassing you could replace it in your class with a
    dictionary of :class:`ReftypeInterface`. Or you can call :meth:`RefobjInterface.register_type` at runtime.
    A type could be "Asset", "Alembic", "Camera" etc.

    Methods to implement:

      * :meth:`RefobjInterface.exists`
      * :meth:`RefobjInterface.get_parent`
      * :meth:`RefobjInterface.set_parent`
      * :meth:`RefobjInterface.get_children`
      * :meth:`RefobjInterface.get_typ`
      * :meth:`RefobjInterface.set_typ`
      * :meth:`RefobjInterface.get_id`
      * :meth:`RefobjInterface.set_id`
      * :meth:`RefobjInterface.create_refobj`
      * :meth:`RefobjInterface.referenced_by`
      * :meth:`RefobjInterface.delete_refobj`
      * :meth:`RefobjInterface.get_all_refobjs`
      * :meth:`RefobjInterface.get_current_element`
      * :meth:`RefobjInterface.set_reference`
      * :meth:`RefobjInterface.get_reference`
      * :meth:`RefobjInterface.get_status`
      * :meth:`RefobjInterface.get_taskfile`

    You might also want to reimplement :meth:`fetch_action_restriction`

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
        """Register a new type with the given interface class

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
    def exists(self, refobj):  #pragma: no cover
        """Check if the given refobj is still in the scene
        or if it has been deleted/dissapeared

        :param refobj: a reference object to query
        :type refobj: refobj
        :returns: True, if it still exists
        :rtype: :class:`bool`
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_parent(self, refobj):  #pragma: no cover
        """Return the refobj of the parent of the given refobj

        :param refobj: a reference object to query
        :type refobj: refobj
        :returns: the parent refobj
        :rtype: refobj | None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_parent(self, child, parent):  #pragma: no cover
        """Set the parent of the child refobj

        E.g. in Maya you would connect the two refobj nodes
        so you can later query the connection when calling
        :meth:`RefobjInterface.get_parent`

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
    def get_children(self, refobj):  #pragma: no cover
        """Get the children refobjects of the given refobject

        It is the reverse query of :meth:`RefobjInterface.get_parent`

        :param refobj: the parent refobj
        :type refobj: refobj
        :returns: a list with children refobjects
        :rtype: list
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_typ(self, refobj):  #pragma: no cover
        """Return the entity type of the given refobject

        See: :data:`RefobjInterface.types`.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the entity type
        :rtype: str
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_typ(self, refobj, typ):  #pragma: no cover
        """Set the type of the given refobj

        :param refobj: the refobj to edit
        :type refobj: refobj
        :param typ: the entity type
        :type typ: str
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_id(self, refobj):  #pragma: no cover
        """Return the identifier of the given refobject

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the refobj id. Used to identify refobjects of the same parent, element and type in the UI
        :rtype: int
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_id(self, refobj, identifier):  #pragma: no cover
        """Set the identifier on the given refobj

        :param refobj: the refobj to edit
        :type refobj: refobj
        :param identifier: the refobj id. Used to identify refobjects of the same parent, element and type in the UI
        :type identifier: int
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_refobj(self, ):  #pragma: no cover
        """Create and return a new refobj

        E.g. in Maya one would create a custom node that can store all
        the necessary information in the scene.
        The type and parent will be set automatically, because one would normally call
        :meth:`RefobjInterface.create`.

        :returns: the new refobj
        :rtype: refobj
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def referenced_by(self, refobj):  #pragma: no cover
        """Return the reference that holds the given refobj.

        Returns None if it is imported/in the current scene.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the reference that holds the given refobj
        :rtype: reference | None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def create(self, typ, identifier, parent=None):
        """Create a new refobj with the given typ and parent

        :param typ: the entity type
        :type typ: str
        :param identifier: the refobj id. Used to identify refobjects of the same parent, element and type in the UI
        :type identifier: int
        :param parent: the parent refobject
        :type parent: refobj
        :returns: The created refobj
        :rtype: refobj
        :raises: None
        """
        refobj = self.create_refobj()
        self.set_typ(refobj, typ)
        self.set_id(refobj, identifier)
        if parent:
            self.set_parent(refobj, parent)
        return refobj

    @abc.abstractmethod
    def delete_refobj(self, refobj):  #pragma: no cover
        """Delete the given refobj

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    def delete(self, refobj):
        """Delete the given refobj and the contents of the entity

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.get_typ_interface(self.get_typ(refobj))
        i.delete(refobj)
        self.delete_refobj(refobj)

    @abc.abstractmethod
    def get_all_refobjs(self, ):  #pragma: no coverg
        """Return all refobjs in the scene

        :returns: all refobjs in the scene
        :rtype: list
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_element(self, ):  #pragma: no cover
        """Return the currently open Shot or Asset

        :returns: the currently open element
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot` | None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_reference(self, refobj, reference):  #pragma: no cover
        """Set the reference of the given refobj to reference

        This will be called by the typinterface after the reference
        has been made. The typinterface should deliver an appropriate
        object as reference that can be used to track the reference
        in the scene.

        :param refobj: the refobj to update
        :type refobj: refobj
        :param reference: the value for the refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reference(self, refobj):  #pragma: no cover
        """Return the reference that the refobj represents or None if it is imported.

        E.g. in Maya this would return the linked reference node.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the reference object in the scene | None
        :raises: None
        """
        raise NotImplementedError

    def reference(self, taskfileinfo, refobj):
        """Reference the given taskfile info and
        set the created reference on the refobj

        This will call :meth:`ReftypeInterface.reference`, then :meth:`ReftypeInterface.set_reference`.

        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :param refobj: the refobj that should represent the new reference
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        ref = inter.reference(refobj, taskfileinfo)
        self.set_reference(refobj, ref)

    def load(self, refobj):
        """Load the given refobject

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        This will call :meth:`ReftypeInterface.load`.

        :param refobj: the refobject
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        ref = self.get_reference(refobj)
        inter.load(refobj, ref)

    def unload(self, refobj):
        """Load the given refobject

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        This will call :meth:`ReftypeInterface.unload`.

        :param refobj: the refobject
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        ref = self.get_reference(refobj)
        inter.unload(refobj, ref)

    def replace(self, refobj, taskfileinfo):
        """Replace the given refobjs reference with the taskfileinfo

        This will call :meth:`ReftypeInterface.replace`.

        :param refobj: the refobject
        :type refobj: refobj
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        ref = self.get_reference(refobj)
        inter.replace(refobj, ref, taskfileinfo)

    def is_replaceable(self, refobj):
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        This will call :meth:`ReftypeInterface.is_replaceable`.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        return inter.is_replaceable(refobj)

    def import_reference(self, refobj):
        """Import the reference of the given refobj

        Here we assume, that the reference is already in the scene and
        we break the encapsulation and pull the data from the reference into
        the current scene.
        This will call :meth:`ReftypeInterface.import_reference` and set the
        reference on the refobj to None.

        :param refobj: the refobj with a reference
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        ref = self.get_reference(refobj)
        inter.import_reference(refobj, ref)
        self.set_reference(refobj, None)

    def import_taskfile(self, refobj, taskfileinfo):
        """Import the given taskfileinfo and update the refobj

        This will call :meth:`ReftypeInterface.import_taskfile`.

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        inter = self.get_typ_interface(self.get_typ(refobj))
        inter.import_taskfile(refobj, taskfileinfo)

    @abc.abstractmethod
    def get_status(self, refobj):  #pragma: no cover
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
    def get_taskfile(self, refobj):  #pragma: no cover
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
        return TaskFileInfo.create_from_taskfile(tf)

    def get_element(self, refobj):
        """Return the element the refobj represents.

        The element is either an Asset or a Shot.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: The element the reftrack represents
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        tf = self.get_taskfile(refobj)
        return tf.task.element

    def fetch_options(self, typ, element):
        """Fetch the options for possible files to
        load replace etc for the given element.

        This will call :meth:`ReftypeInterface.fetch_options`.

        :param typ: the typ of options. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: the option model and a list with all TaskFileInfos
        :rtype: ( :class:`jukeboxcore.gui.treemodel.TreeModel`, list of :class:`TaskFileInfo` )
        :raises: None
        """
        inter = self.get_typ_interface(typ)
        return inter.fetch_options(element)

    def fetch_option_taskfileinfos(self, typ, element):
        """Fetch the options for possible files to load, replace etc for the given element.

        Thiss will call :meth:`ReftypeInterface.fetch_option_taskfileinfos`.

        :param typ: the typ of options. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: The options
        :rtype: list of :class:`TaskFileInfo`
        """
        inter = self.get_typ_interface(typ)
        return inter.fetch_option_taskfileinfos(element)

    def get_option_labels(self, typ, element):
        """Return labels for each level of the option model.

        The options returned by :meth:`RefobjInterface.fetch_options` is a treemodel
        with ``n`` levels. Each level should get a label to describe what is displays.

        E.g. if you organize your options, so that the first level shows the tasks, the second
        level shows the descriptors and the third one shows the versions, then
        your labels should be: ``["Task", "Descriptor", "Version"]``.

        :param typ: the typ of options. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: label strings for all levels
        :rtype: list
        :raises: None
        """
        inter = self.get_typ_interface(typ)
        return inter.get_option_labels(element)

    def get_option_columns(self, typ, element):
        """Return the column of the model to show for each level

        Because each level might be displayed in a combobox. So you might want to provide the column
        to show.

        :param typ: the typ of options. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :param element: The element for wich the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: a list of columns
        :rtype: list
        :raises: None
        """
        inter = self.get_typ_interface(typ)
        return inter.get_option_columns(element)

    def get_suggestions(self, reftrack):
        """Return a list with possible children for this reftrack

        Each Reftrack may want different children. E.g. a Asset wants
        to suggest a shader for itself and all assets that are linked in
        to it in the database. Suggestions only apply for enities with status
        other than None.

        A suggestion is a tuple of typ and element. It will be used to create a newlen
        :class:`Reftrack`. The parent will be this instance, root and interface will
        of course be the same.

        This will delegate the call to the  appropriate :class:`ReftypeInterface`.
        So suggestions may vary for every typ and might depend on the
        status of the reftrack.

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: None
        """
        inter = self.get_typ_interface(reftrack.get_typ())
        return inter.get_suggestions(reftrack)

    def get_typ_icon(self, typ):
        """Get the icon that should be used to identify the type in an UI

        :param typ: the typ. E.g. Asset, Alembic, Camera etc
        :type typ: str
        :returns: a icon for this type
        :rtype: :class:`QtGui.QIcon` | None
        :raises: NotImplementedError
        """
        inter = self.get_typ_interface(typ)
        return inter.get_typ_icon()

    def fetch_action_restriction(self, reftrack, action):
        """Return wheter the given action is restricted for the given reftrack

        available actions are:

           ``reference``, ``load``, ``unload``, ``replace``, ``import_reference``, ``import_taskfile``, ``delete``

        If action is not available, True is returned.

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :param action: the action to check.
        :type action: str
        :returns: True, if the action is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        inter = self.get_typ_interface(reftrack.get_typ())
        d = {'reference': inter.is_reference_restricted, 'load': inter.is_load_restricted,
             'unload': inter.is_unload_restricted, 'replace': inter.is_replace_restricted,
             'import_reference': inter.is_import_ref_restricted, 'import_taskfile': inter.is_import_f_restricted,
             'delete': inter.is_delete_restricted,}
        f = d.get(action, None)
        if not f:
            return True
        else:
            return f(reftrack)

    def get_additional_actions(self, reftrack):
        """Return a list of additional actions you want to provide for the menu
        of the reftrack.

        E.e. you want to have a menu entry, that will select the entity in your programm.

        This will call :meth:`ReftypeInterface.get_additional_actions`.

        The base implementation returns an empty list.

        :param reftrack: the reftrack to return the actions for
        :type reftrack: :class:`Reftrack`
        :returns: A list of :class:`ReftrackAction`
        :rtype: list
        :raises: None
        """
        inter = self.get_typ_interface(reftrack.get_typ())
        return inter.get_additional_actions(reftrack)

    def get_available_types_for_scene(self, element):
        """Return a list of types that can be used in combination with the given element
        to add new reftracks to the scene.

        This allows for example the user, to add new reftracks (aliens) to the scene.
        So e.g. for a shader, it wouldn't make sense to make it available to be added to the scene, because
        one would use them only as children of let's say an asset or cache.
        Some types might only be available for shots or assets etc.

        :param element: the element that could be used in conjuction with the returned types to create new reftracks.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: a list of types
        :rtype: :class:`list`
        :raises: None
        """
        available = []
        for typ, inter in self.types.items():
            if inter(self).is_available_for_scene(element):
                available.append(typ)
        return available


class ReftrackAction(object):
    """A little container for additional actions for
    reftracks. A action can call an arbitrary function, has a name and
    optional an Icon.
    """

    def __init__(self, name, action, icon=None, checkable=False, checked=False, enabled=True):
        """Initialize a new action with the given name, actionfunction and optional an icon

        :param name: the name of the action. Will be shown in GUIs
        :type name: str
        :param action: the function that should be called when the action is triggered.
        :type action: callable
        :param icon: Optional Icon for GUIs
        :type icon: :class:`QtGui.QIcon`
        :param checkable: If true, the action will be checkable in the UI
        :type checkable: :class:`bool`
        :param checked: If True, the action wil be checked by default
        :type checked: :class:`bool`
        :param eneabled: Whether the action should be enabled
        :type eneabled: :class:`bool`
        :raises: None
        """
        self.name = name
        self.action = action
        self.icon = icon
        self.checkable = checkable
        self.checked = checked
        self.enabled = enabled


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
      * :meth:`ReftypeInterface.fetch_option_taskfileinfos`
      * :meth:`ReftypeInterface.create_options_model`
      * :meth:`ReftypeInterface.get_suggestions`
      * :meth:`ReftypeInterface.get_option_labels`
      * :meth:`ReftypeInterface.get_option_columns`
      * :meth:`ReftypeInterface.is_available_for_scene`

    You might also want to reimplement:

      * :meth:`ReftypeInterface.get_typ_icon`
      * :meth:`ReftypeInterface.get_scene_suggestions`
      * :meth:`ReftypeInterface.is_reference_restricted`
      * :meth:`ReftypeInterface.is_load_restricted`
      * :meth:`ReftypeInterface.is_unload_restricted`
      * :meth:`ReftypeInterface.is_import_ref_restricted`
      * :meth:`ReftypeInterface.is_import_f_restricted`
      * :meth:`ReftypeInterface.is_replace_restricted`
      * :meth:`ReftypeInterface.get_additional_actions`

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
    def reference(self, refobj, taskfileinfo):  #pragma: no cover
        """Reference the given taskfileinfo into the scene and return the created reference object

        The created reference object will be used on :meth:`RefobjInterface.set_reference` to
        set the reference on a refobj. E.g. in Maya, one would return the reference node
        so the RefobjInterface can link the refobj with the refernce object.
        Do not call :meth:`RefobjInterface.set_reference` yourself.

        :param refobj: the refobj that will be linked to the reference
        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: the reference that was created and should set on the appropriate refobj
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, refobj, reference):  #pragma: no cover
        """Load the given reference

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def unload(self, refobj, reference):  #pragma: no cover
        """Unload the given reference

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, refobj, reference, taskfileinfo):  #pragma: no cover
        """Replace the given reference with the given taskfileinfo

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, refobj):  #pragma: no cover
        """Delete the content of the given refobj

        :param refobj: the refobj that represents the content that should be deleted
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def import_reference(self, refobj, reference):  #pragma: no cover
        """Import the given reference

        The reference of the refobj will be set to None automatically afterwards with
        :meth:`RefobjInterface.set_reference`

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def import_taskfile(self, refobj, taskfileinfo):  #pragma: no cover
        """Import the given taskfileinfo and update the refobj

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_replaceable(self, refobj):  #pragma: no cover
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def fetch_options(self, element):
        """Fetch the options for possible files to
        load replace etc for the given element.

        Options from which to choose a file to load or replace.
        The options are a :class:`jukeboxcore.gui.treemodel.TreeModel`
        with :class:`jukeboxcore.filesys.TaskFileInfo` as leafes internal data.
        I explicitly say leafes because the options might be sorted in a tree like strucure.
        So the user could first select a task and then the apropriate release.
        You can take the model and display it to the user so he can select a file.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: the option model and a list with all TaskFileInfos
        :rtype: ( :class:`jukeboxcore.gui.treemodel.TreeModel`, list of :class:`TaskFileInfo` )
        :raises: None
        """
        tfis = self.fetch_option_taskfileinfos(element)
        return self.create_options_model(tfis), tfis

    @abc.abstractmethod
    def fetch_option_taskfileinfos(self, element):  #pragma: no cover
        """Fetch the options for possible files to load, replace etc for the given element.

        Options from which to choose a file to load or replace.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: The options
        :rtype: list of :class:`TaskFileInfo`
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_options_model(self, taskfileinfos):  #pragma: no cover
        """Create a new treemodel that has the taskfileinfos as internal_data of the leaves.

        I recommend using :class:`jukeboxcore.gui.filesysitemdata.TaskFileInfoItemData` for the leaves.
        So a valid root item would be something like::

          rootdata = jukeboxcore.gui.treemodel.ListItemData(["Asset/Shot", "Task", "Descriptor", "Version", "Releasetype"])
          rootitem = jukeboxcore.gui.treemodel.TreeItem(rootdata)

        :returns: the option model with :class:`TaskFileInfo` as internal_data of the leaves.
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_option_labels(self, element):  #pragma: no cover
        """Return labels for each level of the option model.

        The options returned by :meth:`RefobjInterface.fetch_options` is a treemodel
        with ``n`` levels. Each level should get a label to describe what is displays.

        E.g. if you organize your options, so that the first level shows the tasks, the second
        level shows the descriptors and the third one shows the versions, then
        your labels should be: ``["Task", "Descriptor", "Version"]``.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: label strings for all levels
        :rtype: list
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_option_columns(self, element):  #pragma: no cover
        """Return the column of the model to show for each level

        Because each level might be displayed in a combobox. So you might want to provide the column
        to show.

        :param element: The element for wich the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: a list of columns
        :rtype: list
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_suggestions(self, reftrack):  #pragma: no cover
        """Return a list with possible children for this reftrack

        Each Reftrack may want different children. E.g. a Asset wants
        to suggest a shader for itself and all assets that are linked in
        to it in the database. Suggestions only apply for enities with status
        other than None.

        A suggestion is a tuple of typ and element. It will be used to create a newlen
        :class:`Reftrack`. The parent will be this instance, root and interface will
        of course be the same.

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: NotImplementedError
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_available_for_scene(self, element):
        """Return True, if it should be possible to add a new reftrack with the given
        element and the type of the interface to the scene.

        Some types might only make sense for a shot or asset. Others should never be available, because
        you would only use them as children of other reftracks (e.g. a shader).

        :param element: the element that could be used in conjuction with the returned types to create new reftracks.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: True, if available
        :rtype: :class:`bool`
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def get_typ_icon(self, ):
        """Return a icon that should be used to identify the type in an UI

        :returns: a icon for this type
        :rtype: :class:`QtGui.QIcon` | None
        :raises: NotImplementedError
        """
        return None

    def get_scene_suggestions(self, current):
        """Return a list with elements for reftracks for the current scene with this type.

        For every element returned, the reftrack system will create a :class:`Reftrack` with the type
        of this interface, if it is not already in the scene.

        E.g. if you have a type that references whole scenes, you might suggest all
        linked assets for shots, and all liked assets plus the current element itself for assets.
        If you have a type like shader, that usually need a parent, you would return an empty list.
        Cameras might only make sense for shots and not for assets etc.

        Do not confuse this with :meth:`ReftypeInterface.get_suggestions`. It will gather suggestions
        for children of a :class:`Reftrack`.

        The standard implementation only returns an empty list!

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: None
        """
        return []

    def is_reference_restricted(self, reftrack):
        """Return whether referencing for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_load_restricted(self, reftrack):
        """Return whether loading for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_unload_restricted(self, reftrack):
        """Return whether unloading for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_import_ref_restricted(self, reftrack):
        """Return whether importing the reference for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_import_f_restricted(self, reftrack):
        """Return whether importing a file for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_replace_restricted(self, reftrack):
        """Return whether replacing for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def is_delete_restricted(self, reftrack):
        """Return whether deleting for the given reftrack should be restricted

        This implementation returns always False

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :returns: True, if restricted
        :rtype: :class:`bool`
        :raises: None
        """
        return False

    def get_additional_actions(self, reftrack):
        """Return a list of additional actions you want to provide for the menu
        of the reftrack.

        E.e. you want to have a menu entry, that will select the entity in your programm.

        The base implementation returns an empty list.

        :param reftrack: the reftrack to return the actions for
        :type reftrack: :class:`Reftrack`
        :returns: A list of :class:`ReftrackAction`
        :rtype: list
        :raises: None
        """
        return []
