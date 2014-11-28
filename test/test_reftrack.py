"""Tets the functionality of the :mod:`jukeboxcore.reftrack` module"""
from jukeboxcore.reftrack import Reftrack, RefobjInterface, ReftypeInterface
from jukeboxcore import djadapter
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.treemodel import TreeItem, TreeModel, ListItemData
from jukeboxcore.gui.filesysitemdata import TaskFileInfoItemData


class Reference(object):
    """A dummy reference object that does nothing but just tells
    if it is currently loaded or unloaded
    """

    def __init__(self, loaded=True):
        """Initialize a new reference with the given status

        :param loaded: True if loaded, false if unloaded
        :type loaded: :class:`bool`
        :raises: None
        """
        self.loaded = loaded


class Refobj(object):
    """An refobj for testing with a refobject interface

    The :class:`RefobjInterface` is abstract and we need some kind of object for testing.
    This refobj stores type, status, parent, a reference, the taskfile.
    """

    instances = []

    def __init__(self, typ, parent, reference, taskfile, referenced):
        """Initialize a new refobj

        :param typ: the type of the entity
        :type typ: str
        :param parent: the parent refobj
        :type parent: :class:`Refobj` | None
        :param reference: the reference object
        :type reference: :class:`Referencce`
        :param taskfile: the taskfile that is loaded
        :type taskfile: :class:`jukeboxcore.djadapter.models.TaskFile`
        :param referenced: True, if this refobj was referenced by some reference
        :type referenced: :class:`bool`
        :rtype: None
        :raises: None
        """
        self.instances.append(self)
        self.typ = typ
        self.parent = parent
        self.children = []
        parent.children.append(self)
        self.reference = reference
        self.taskfile = taskfile
        self.referenced = referenced

    def get_status(self, ):
        """Return the status

        :returns: the status, loaded, unloaded, imported
        :rtype: str
        :raises: None
        """
        if not self.reference:
            return Reftrack.IMPORTED
        else:
            if self.reference.loaded:
                return Reftrack.LOADED
            else:
                return Reftrack.UNLOADED


class TestRefobjInterface(RefobjInterface):
    """A implementation for the refobjinterface for testing

    uses :class:`Refobj` as refobjects
    """

    def __init__(self, current):
        """

        :param current: the current shot or element that is open
        :type current: Shot or Asset
        :raises: None
        """
        super(TestRefobjInterface, self).__init__()
        self.current = current

    def get_parent(self, refobj):
        """Return the parent

        :param refobj: the refobj to query
        :type refobj: :class:`Refobj`
        :returns: the parent
        :rtype: :class:`Refobj`
        :raises: None
        """
        return refobj.parent

    def set_parent(self, refobj, parent):
        """Set the parent

        :param refobj: the refobj to edit
        :type refobj: :class:`Refobj`
        :param parent: the new parent
        :type parent: :class:`Refobj`
        :returns: None
        :rtype: None
        :raises: None
        """
        if refobj.parent:
            refobj.parent.children.remove(refobj)
        refobj.parent = parent
        parent.children.append(refobj)

    def get_children(self, refobj):
        """Return the children of the refobj

        :param refobj: the refobj to query
        :type refobj: :class:`Refobj`
        :returns: the children
        :rtype: list of refobjects
        :raises: None
        """
        return refobj.children

    def get_typ(self, refobj):
        """Return the entity type of the given refobject

        See: :data:`RefobjInterface.types`.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the entity type
        :rtype: str
        :raises: None
        """
        return refobj.typ

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
        refobj.typ = typ

    def create_refobj(self, ):
        """Create and return a new refobj

        E.g. in Maya one would create a custom node that can store all
        the necessary information in the scene.
        The type and parent will be set automatically, because one would normally call
        :meth:`RefobjInterface.create`.

        :returns: the new refobj
        :rtype: refobj
        :raises: None
        """
        return Refobj(None, None, None, None, False)

    def referenced(self, refobj):
        """Return whether the given refobj is referenced.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: True if referenced, False if imported
        :rtype: None
        :raises: None
        """
        return refobj.referenced

    def delete_refobj(self, refobj):
        """Delete the given refobj

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        if refobj.parent:
            refobj.parent.children.remove(refobj)
        Refobj.instances.remove(refobj)

    def get_all_refobjs(self, ):
        """Return all refobjs in the scene that are not referenced

        We do not support nested references at the moment!
        So filter them with :meth:`RefobjInterface.is_referenced`.

        :returns: all refobjs in the scene
        :rtype: list
        :raises: None
        """
        return filter(self.is_referenced, Refobj.instances)

    def get_current_element(self, ):
        """Return the currenty open Shot or Asset

        :returns: the currently open element
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot` | None
        :raises: None
        """
        return self.current

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
        refobj.reference = reference

    def get_reference(self, refobj):
        """Return the reference that the refobj represents or None if it is imported.

        E.g. in Maya this would return the linked reference node.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the reference object in the scene | None
        :raises: None
        """
        return refobj.reference

    def get_status(self, refobj):
        """Return the status of the given refobj

        See: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the status of the given refobj
        :rtype: str
        :raises: None
        """
        return refobj.get_status()

    def get_taskfile(self, refobj):
        """Return the taskfile that is loaded and represented by the refobj

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: The taskfile that is loaded in the scene
        :rtype: :class:`jukeboxcore.djadapter.TaskFile`
        :raises: None
        """
        return refobj.taskfile


class AssetReftypeInterface(ReftypeInterface):
    """Implementation for the reftype interface for testing
    for the type asset
    """

    def __init__(self, refobjinter):
        """Initialize a new ReftypeInterface

        :param refobjinter: the refobject interface
        :type refobjinter: :class:`RefobjInterface`
        :raises: None
        """
        super(AssetReftypeInterface, self).__init__(refobjinter)

    def reference(self, refobj, taskfileinfo):
        """Reference the given taskfileinfo into the scene and return the created reference object

        The created reference object will be used on :meth:`RefobjInterface.set_reference` to
        set the reference on a refobj. E.g. in Maya, one would return the reference node
        so the RefobjInterface can link the refobj with the refernce object.

        :param refobj: the refobj
        :type refobj: :class:`Refobj`
        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: the reference that was created and should set on the appropriate refobj
        :raises: NotImplementedError
        """
        ref = Reference()
        refobj.taskfile = djadapter.taskfiles.get(task=taskfileinfo.task,
                                        version=taskfileinfo.version,
                                        releasetype=taskfileinfo.releasetype,
                                        descriptor=taskfileinfo.descriptor,
                                        typ=taskfileinfo.typ)
        return ref

    def load(self, refobj, reference):
        """Load the given reference

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        :param refobj: the refobj
        :type refobj: :class:`Refobj`
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        reference.loaded = True

    def unload(self, refobj, reference):
        """Unload the given reference

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        :param refobj: the refobj
        :type refobj: :class:`Refobj`
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        reference.loaded = False

    def replace(self, refobj, reference, taskfileinfo):
        """Replace the given reference with the given taskfileinfo

        :param refobj: the refobj
        :type refobj: :class:`Refobj`
        :param reference: the reference object. E.g. in Maya a reference node
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        refobj.taskfile = djadapter.taskfiles.get(task=taskfileinfo.task,
                                        version=taskfileinfo.version,
                                        releasetype=taskfileinfo.releasetype,
                                        descriptor=taskfileinfo.descriptor,
                                        typ=taskfileinfo.typ)

    def delete(self, refobj):
        """Delete the content of the given refobj

        :param refobj: the refobj that represents the content that should be deleted
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        pass

    def import_reference(self, refobj, reference):
        """Import the given reference

        :param refobj: the refobj
        :type refobj: :class:`Refobj`
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        pass

    def import_taskfile(self, refobj, taskfileinfo):
        """Import the given taskfileinfo and update the refobj

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        refobj.taskfile = djadapter.taskfiles.get(task=taskfileinfo.task,
                                        version=taskfileinfo.version,
                                        releasetype=taskfileinfo.releasetype,
                                        descriptor=taskfileinfo.descriptor,
                                        typ=taskfileinfo.typ)

    def is_replaceable(self, refobj):
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: NotImplementedError
        """
        return True

    def fetch_option_taskfileinfos(self, element):
        """Fetch the options for possible files to load, replace etc for the given element.

        Options from which to choose a file to load or replace.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: The options
        :rtype: list of :class:`TaskFileInfo`
        :raises: NotImplementedError
        """
        tfs = djadapter.taskfiles.filter(task__element=element,
                                         typ=djadapter.FILETYPES['mayamainscene'],
                                         releasetype=djadapter.RELEASETYPES['release'])
        l = []
        for tf in tfs:
            tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype, descriptor=tf.descriptor, typ=tf.typ)
            l.append(tfi)
        return l

    def create_options_model(self, taskfileinfos):
        """Create a new treemodel that has the taskfileinfos as internal_data of the leaves.

        I recommend using :class:`jukeboxcore.gui.filesysitemdata.TaskFileInfoItemData` for the leaves.
        So a valid root item would be something like::

          rootdata = jukeboxcore.gui.treemodel.ListItemData(["Asset/Shot", "Task", "Descriptor", "Version", "Releasetype"])
          rootitem = jukeboxcore.gui.treemodel.TreeItem(rootdata)

        :returns: the option model with :class:`TaskFileInfo` as internal_data of the leaves.
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: NotImplementedError
        """
        rootdata = ListItemData(["Asset/Shot", "Task", "Descriptor", "Version", "Releasetype"])
        rootitem = TreeItem(rootdata)
        for tfi in taskfileinfos:
            tfidata = TaskFileInfoItemData(tfi)
            TreeItem(tfidata, parent=rootitem)
        return TreeModel(rootitem)
