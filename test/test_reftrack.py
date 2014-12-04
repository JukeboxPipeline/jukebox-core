"""Tets the functionality of the :mod:`jukeboxcore.reftrack` module"""
import pytest
import mock

from jukeboxcore.reftrack import Reftrack, RefobjInterface, ReftypeInterface, ReftrackRoot
from jukeboxcore import djadapter
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.treemodel import TreeItem, TreeModel, ListItemData
from jukeboxcore.gui.filesysitemdata import TaskFileInfoItemData
from django.contrib.contenttypes.models import ContentType


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

    def __init__(self, typ, parent, reference, taskfile, referencedby):
        """Initialize a new refobj

        :param typ: the type of the entity
        :type typ: str
        :param parent: the parent refobj
        :type parent: :class:`Refobj` | None
        :param reference: the reference object
        :type reference: :class:`Referencce`
        :param taskfile: the taskfile that is loaded
        :type taskfile: :class:`jukeboxcore.djadapter.models.TaskFile`
        :param referencedby: The reference that holds this refobj.
        :type referencedby: :class:`Reference` | None
        :rtype: None
        :raises: None
        """
        self.instances.append(self)
        self.typ = typ
        self.parent = parent
        self.deleted = False
        self.children = []
        if parent:
            parent.children.append(self)
        self.reference = reference
        self.taskfile = taskfile
        self.referencedby = referencedby

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


class DummyRefobjInterface(RefobjInterface):
    """A implementation for the refobjinterface for testing

    uses :class:`Refobj` as refobjects
    """

    def __init__(self, current):
        """

        :param current: the current shot or element that is open
        :type current: Shot or Asset
        :raises: None
        """
        super(DummyRefobjInterface, self).__init__()
        self.current = current

    def exists(self, refobj):
        """Check if the given refobj is still in the scene
        or if it has been deleted/dissapeared

        :param refobj: a reference object to query
        :type refobj: refobj
        :returns: True, if it still exists
        :rtype: :class:`bool`
        :raises: None
        """
        return not refobj.deleted

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
        if parent:
            parent.children.append(refobj)
        refobj.parent = parent

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

    def referenced_by(self, refobj):
        """Return the reference that holds the given refobj.

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: The reference
        :rtype: :class:`Reference` | None
        :raises: None
        """
        return refobj.referencedby

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

        :returns: all refobjs in the scene
        :rtype: list
        :raises: None
        """
        return Refobj.instances

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
        refobj.deleted = True

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
        tfs = djadapter.taskfiles.filter(task__content_type=ContentType.objects.get_for_model(element),
                                         task__object_id=element.pk,
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

    def get_suggestions(self, reftrack):
        """Return a list with possible children for this reftrack

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: NotImplementedError
        """
        element = reftrack.get_element()
        elements = list(element.assets.all())
        elements.append(element)
        typ = reftrack.get_typ()
        return [(typ, e) for e in elements]

RefobjInterface.register_type('Asset', AssetReftypeInterface)


@pytest.fixture(scope='function', autouse=True)
def refobjclass(request):
    def fin():
        Refobj.instances = []
    request.addfinalizer(fin)


@pytest.fixture(scope='function')
def reftrackroot():
    return ReftrackRoot()


@pytest.fixture(scope='function')
def refobjinter(djprj):
    current = djprj.shots[0]
    return DummyRefobjInterface(current)


def test_wrap(djprj, reftrackroot, refobjinter):
    l = []
    for tf in djprj.assettaskfiles[:6]:
        refobj = Refobj('Asset', None, None, tf, False)
        l.append(refobj)
    l[0].parent = l[1]
    l[2].parent = l[1]
    l[3].parent = l[2]
    l[1].parent = l[4]

    tracks = Reftrack.wrap(reftrackroot, refobjinter, l)
    assert tracks[0].get_parent() is tracks[1]
    assert tracks[1].get_parent() is tracks[4]
    assert tracks[2].get_parent() is tracks[1]
    assert tracks[3].get_parent() is tracks[2]
    assert tracks[4].get_parent() is None

    for t in tracks:
        assert t.get_typ() == 'Asset'
        assert t is reftrackroot.get_reftrack(t.get_refobj())
        assert t.status() == Reftrack.IMPORTED
        # assert if suggestions have been created
        suggestions = t.get_suggestions()
        for c in t._children:
            for i, (typ, element) in enumerate(suggestions):
                if c.get_typ() == typ and c.get_element() == element:
                    del suggestions[i]
                    break
        assert suggestions == [],\
            "Not all suggestions were created after wrapping. Suggestions missing %s" % suggestions


def test_create_empty(djprj, reftrackroot, refobjinter):
    r1 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[0])
    r2 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[1], parent=r1)
    assert r1 in reftrackroot._reftracks
    assert r2 in reftrackroot._reftracks
    assert r2.get_treeitem().parent() is r1.get_treeitem()
    assert r2.get_parent() is r1
    assert r1.status() is None
    assert r2.status() is None
    assert not r1.alien()
    assert r2.alien()
    assert r1.get_typ() == 'Asset'
    assert r2.get_typ() == 'Asset'


def test_alien(djprj, reftrackroot):
    current = djprj.assets[0]
    refobjinter = DummyRefobjInterface(current)
    r1 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[0])
    r2 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[1])
    r3 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[1], parent=r2)
    assert not r1.alien()
    assert r2.alien()
    assert not r3.alien()


@mock.patch.object(AssetReftypeInterface, "get_suggestions")
def test_delete(mock_suggestions, djprj, reftrackroot):
    mock_suggestions.returnvalue = []
    current = djprj.assets[0]
    refobjinter = DummyRefobjInterface(current)
    ref0 = Reference()
    ref1 = Reference()
    ref2 = Reference()
    ref4 = Reference()
    robj0 = Refobj('Asset', None, ref0, djprj.assettaskfiles[-1], None)
    robj1 = Refobj('Asset', robj0, ref1, djprj.assettaskfiles[0], ref0)
    robj2 = Refobj('Asset', robj1, ref2, djprj.assettaskfiles[0], ref1)
    robj3 = Refobj('Asset', robj2, None, djprj.assettaskfiles[0], None)
    robj4 = Refobj('Asset', robj0, ref4, djprj.assettaskfiles[0], None)
    robj5 = Refobj('Asset', robj4, None, djprj.assettaskfiles[0], ref0)
    robj6 = Refobj('Asset', robj4, None, djprj.assettaskfiles[0], None)
    tracks = Reftrack.wrap(reftrackroot, refobjinter, [robj0, robj1, robj2, robj3, robj4, robj5, robj6])

    assert tracks[0].get_all_children() == [tracks[1], tracks[4], tracks[2], tracks[5], tracks[6], tracks[3]]
    assert tracks[6].get_all_children() == []
    assert tracks[4].get_all_children() == [tracks[5], tracks[6]]
    assert tracks[2].get_children_to_delete() == [tracks[3]]
    assert tracks[0].get_children_to_delete() == [tracks[4], tracks[6], tracks[3]]
    assert tracks[4].get_children_to_delete() == [tracks[5], tracks[6]]

    tracks[2].delete()
    assert tracks[2]._children == []
    assert tracks[2].get_refobj() is None
    assert tracks[2] in reftrackroot._reftracks
    assert tracks[3].get_refobj() is None
    assert tracks[3] not in reftrackroot._reftracks
    assert tracks[3].get_parent() is None
    assert robj3.deleted

    assert tracks[0].alien()
    tracks[0].delete()
    assert robj4.deleted
    assert robj0.deleted
    for i, t in enumerate(tracks):
        assert t not in reftrackroot._reftracks


def test_duplicate(djprj, reftrackroot, refobjinter):
    ref = Reference()
    robj0 = Refobj('Asset', None, ref, djprj.assettaskfiles[0], None)
    robj1 = Refobj('Asset', robj0, None, djprj.assettaskfiles[0], None)
    tracks = Reftrack.wrap(reftrackroot, refobjinter, [robj0, robj1])
    tracks.append(Reftrack(root=reftrackroot,
                           refobjinter=refobjinter,
                           typ='Asset',
                           element=djprj.assettaskfiles[1],
                           parent=tracks[1]))
    for t in tracks:
        d = t.duplicate()
        assert d.get_root() is t.get_root()
        assert d.get_refobjinter() is t.get_refobjinter()
        assert d.get_typ() is t.get_typ()
        assert d.get_element() is t.get_element()
        assert d.get_parent() is t.get_parent()
        assert d.status() is None
        assert d.get_treeitem().parent() is t.get_treeitem().parent()


def test_throw_children_away(djprj, reftrackroot, refobjinter):
    robj0 = Refobj('Asset', None, None, djprj.assettaskfiles[0], None)
    robj1 = Refobj('Asset', robj0, None, djprj.assettaskfiles[0], None)
    robj2 = Refobj('Asset', robj1, None, djprj.assettaskfiles[0], None)
    robj3 = Refobj('Asset', None, None, djprj.assettaskfiles[0], None)
    tracks = Reftrack.wrap(reftrackroot, refobjinter, [robj0, robj1, robj2, robj3])

    tracks[0].throw_children_away()

    assert tracks[0]._children == []
    assert tracks[1].get_parent() is None
    assert tracks[1].get_treeitem().parent() is None
    assert tracks[1].get_treeitem()._model is None
    assert tracks[0].get_treeitem().child_count() == 0
    assert tracks[1] not in reftrackroot._reftracks
    assert tracks[2] not in reftrackroot._reftracks
    assert tracks[3] in reftrackroot._reftracks
    assert refobjinter.exists(tracks[1].get_refobj())
    assert refobjinter.exists(tracks[2].get_refobj())


def test_fetch_new_children(djprj, reftrackroot, refobjinter):
    robj0 = Refobj('Asset', None, None, djprj.assettaskfiles[0], None)
    t0 = Reftrack.wrap(reftrackroot, refobjinter, [robj0])[0]
    robj1 = Refobj('Asset', None, None, djprj.assettaskfiles[0], None)
    t1 = Reftrack.wrap(reftrackroot, refobjinter, [robj1])[0]
    t0.throw_children_away()
    assert t0 in reftrackroot._reftracks
    assert t1 in reftrackroot._reftracks
    assert t0.get_refobj() in reftrackroot._parentsearchdict
    assert t1.get_refobj() in reftrackroot._parentsearchdict

    robj2 = Refobj('Asset', robj0, None, djprj.assettaskfiles[0], None)
    robj3 = Refobj('Asset', robj2, None, djprj.assettaskfiles[0], None)
    t2, t3 = Reftrack.wrap(reftrackroot, refobjinter, [robj2, robj3])
    t0.throw_children_away()
    for t in (t2, t3):
        assert t not in reftrackroot._reftracks
        assert t.get_refobj() not in reftrackroot._parentsearchdict
        assert refobjinter.exists(t.get_refobj())
    assert t2.get_parent() is None
    assert t2.get_treeitem().parent() is None
    # try wrapping them again
    Reftrack.wrap(reftrackroot, refobjinter, [robj2, robj3])


def test_create_refobject(djprj, reftrackroot, refobjinter):
    robj0 = Refobj('Asset', None, None, djprj.assettaskfiles[0], None)
    t0 = Reftrack.wrap(reftrackroot, refobjinter, [robj0])[0]
    t1 = Reftrack(reftrackroot, refobjinter, typ='Asset', element=djprj.assets[0], parent=t0)
    robj1 = t1.create_refobject()
    assert robj1.parent is robj0
    assert robj1.typ == 'Asset'

