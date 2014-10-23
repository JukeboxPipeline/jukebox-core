import os
from operator import attrgetter

from django.db.models import Max

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore import djadapter as dj


class FileElement(object):
    """A file element uses a file info object to retrieve some information and generate
    part of the path or name of a file. This Class is meant to be used as a
    baseclass. Override at least one of the functions:

      :meth:`FileElement.get_dir`
      :meth:`FileElement.get_chunk`

    A filepath consists of multiple directories. Each element can, but must not, contribute
    to this path.
    A filename consits of multiple chunks, that are seperated by underscores.
    """

    def get_dir(self, obj):
        """Return a part of the filepath for the given object, or none if the element
        does not contribute a directory.

        Some Elements might only add a chunk to the filename. These elements should
        always return ``None``.
        Each element is responsible for a certain aspect/attribute of the obj and
        uses this attribute to generate part of the filepath.
        E.g. an element, that creates a folder for every version of obj, could return
        a string like ``'v###'`` with the version numbers inserted.
        A element that is responsible for the project, might return the complete root path
        for that objects project.

        The default will return None. So override it if necessary.

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: a part of the filepath or None
        :rtype: str|None
        :raises: None
        """
        return None

    def get_chunk(self, obj):
        """Return a filename chunk, or None if the element
        does not contribute to the filename.

        Some Elements might only add a directory to the filepath. These elements should
        always return ``None``.
        Each element is responsible for a certain aspect/attribute of the obj and
        uses this attribute to generate part of the filename (chunk).
        Chunks are seperated by underscores and should not contain any spaces.
        E.g. an element that inserts the username to the filename might return
        the username as a string.

        The default will return None. So override it if necessary.

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: a filename chunk or None
        :rtype: str|None
        :raises: None
        """
        return None


class StaticElement(FileElement):
    """A static element that will always give the same dir or chunk and is independent of the object

    Can be used to insert static folders like a folder where all maya files go.
    """

    def __init__(self, dirname=None, chunk=None):
        """Constructs a new static element that will always give the specified dir and/or chunk

        :param dirname: the dirname the element will contribute or None
        :type dirname: str|None
        :param chunk: the chunk for the filename the element will contribute or None
        :type chunk: str|None
        :raises: None
        """
        super(StaticElement, self).__init__()
        self._dirname = dirname
        self._chunk = chunk

    def get_dir(self, obj):
        """Return a part of the filepath for the given object, or None if the element
        does not contribute a directory.

        This will always return the dirname that was specified in the constructor

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: the directory that was given in the constructor
        :rtype: str|None
        :raises: None
        """
        return self._dirname

    def get_chunk(self, obj):
        """Return a filenamechunk or None, if the element
        does not contribute a directory

        This will always return the chunk that was specified in the constructor

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: the chunk that was given in the contructor
        :rtype: str|None
        :raises: None
        """
        return self._chunk


class AttrElement(FileElement):
    """A simple element that will always return a certain attribute for a dir or chunk

    You can also specify a format string.
    """

    def __init__(self, dirattr=None, chunkattr=None, dirformat='%s', chunkformat='%s'):
        """Constructs a new attr element. It will use the given attribute to query with ``operator.attrgetter``
        and format it with the corresponding format string. So it is possible to get nested attributes.
        For nested attributes specify something like this: ``attr1.attr2.attr3``.

        :param dirattr: the attribute to use for directories
        :type dirattr: str|None
        :param chunkattr: the attribute to use for chunks
        :type chunkattr: str|None
        :param dirformat: the format string for directories. formating will be done with the ``%`` operator.
        :type dirformat: str
        :param chunkformat: the format string for chunks. formating will be done with the ``%`` operator.
        :type chunkformat: str
        :raises: None
        """
        super(AttrElement, self).__init__()
        self._dirattr = dirattr
        self._chunkattr = chunkattr
        self._dirformat = dirformat
        self._chunkformat = chunkformat

    def get_dir(self, obj):
        """Return the dirattr of obj formatted with the dirfomat specified in the constructor.
        If the attr is None then ``None`` is returned not the string ``\'None\'``.

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: the directory or None
        :rtype: str|None
        :raises: None
        """
        if self._dirattr is None:
            return
        a = attrgetter(self._dirattr)(obj)
        if a is None:
            return
        s = self._dirformat % a
        return s

    def get_chunk(self, obj):
        """Return the chunkattr of obj formatted with the chunkfomat specified in the constructor
        If the attr is None then ``None`` is returned not the string ``\'None\'``.

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: the chunk or None
        :rtype: str|None
        :raises: None
        """
        if self._chunkattr is None:
            return
        a = attrgetter(self._chunkattr)(obj)
        if a is None:
            return
        s = self._chunkformat % a
        return s


class SoftwareElement(FileElement):
    """This element checks a TaskFileInfo for the typ and returns the directory name
    for the software branch.
    """
    def get_dir(self, taskinfo):
        """Return a directory for the software, depending on the typ of taskinfo

        :param obj: the fileinfo with information.
        :type obj: :class:`TaskFileInfo`
        :returns: directory for the software, depending on the typ of taskinfo
        :rtype: str
        :raises: None
        """
        if taskinfo.typ == taskinfo.TYPES['mayamainscene']:
            return 'Maya'


class TaskGroupElement(FileElement):
    """This element checks a TaskFileInfo and returns the top directory name
    for either shots or assets joined by either the sequence name or the assettype name
    """
    def get_dir(self, taskinfo):
        """Return ``assets/`` + assettypename if it is for an assettask or ``shots/`` + sequencename if is is for a shottask

        :param obj: the fileinfo with information.
        :type obj: :class:`TaskFileInfo`
        :returns: ``assets`` or ``shots`` depending on the assetflag of the task of taskinfo
        :rtype: str
        :raises: None
        """
        if taskinfo.task.department.assetflag:
            atname = taskinfo.task.element.atype.name
            d = os.path.join('assets', atname)
            return d
        else:
            seqname = taskinfo.task.element.sequence.name
            d = os.path.join('shots', seqname)
            return d


class ExtElement(object):
    """The ExtElement uses a file info object to determine the file extension
    """

    def get_ext(self, obj):
        """Return a file extension (without the extension seperator) for the given file info obj

        :param obj: the fileinfo with information.
        :type obj: :class:`TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        raise NotImplementedError


class StaticExtElement(ExtElement):
    """This extension element will always return the same extension no matter what the file info is"""

    def __init__(self, ext):
        """Constructs a new static extension element that always returns the given file extension

        :param ext: the extension
        :type ext: str
        :raises: None
        """
        self._ext = ext

    def get_ext(self, obj):
        """

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: the extension that was specified in the constructor
        :rtype: str
        :raises: None
        """
        return self._ext


class TaskFileExtElement(ExtElement):
    """This extension element uses a :class:`TaskFileInfo` and returns an appropriate extension"""

    def get_ext(self, taskinfo):
        """Return a file extension (without the extension seperator) for the given file info obj

        :param obj: the fileinfo with information.
        :type obj: :class:`TaskFileInfo`
        :returns: the appropriate extension without extension seperator (``.``)
        :rtype: str
        :raises: None
        """
        if taskinfo.typ == taskinfo.TYPES['mayamainscene']:
            return 'mb'


class FileInfo(object):
    """Abstract class that can be used for implementing info objects
    that can be used with FileElements

    You don't have to use this, but it provides an interface for
    getting the latest or next version.
    """

    @classmethod
    def get_latest(cls, ):
        """Get the latest existing file for the given info or None if there is no existing one

        You should reimplement this method so it accepts
        some arguments with infos and returns
        a FileInfo that is the latest version
        for the given info.

        :returns: a fileinfoobject that is the latest existing file for the given info
        :rtype: :class:`FileInfo` | None
        :raises: None
        """
        raise NotImplementedError

    @classmethod
    def get_next(cls, ):
        """Return a file info object that would be the next version for the given info

        You should reimplement this method so it accepts
        some arguments with infos and returns
        a FileInfo that would be the next version after the latest
        for the given info

        :returns: a fileinfoobject that is the latest existing file for the given info
        :rtype: :class:`FileInfo`
        :raises: None
        """
        raise NotImplementedError


class TaskFileInfo(FileInfo):
    """FileInfo for a taskfile

    Can get the latest or the next version if you provide a task, releasetype (and a descriptor).
    """

    TYPES = dj.FILETYPES
    """A dict for file types that can be used in a TaskFile

    the values are the actual data that gets stored in the database.

    Explanations:

      :mayamainscene: probably the most common for maya scenes. these are the usual release and workfiles
                      maybe even a handoff file, if it does not need a direct subfolder.
                      Main scenes hold the main information, not just extracted parts.
                      If you export shader or maybe some blendshapes in a scene, do not use this one.
    """

    def __init__(self, task, version, releasetype, typ, descriptor=None):
        """Constructs a new TaskFileInfo

        :param task: the task of the taskfile
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :param version: the version of the TaskFile
        :type version: int
        :param releasetype: the releasetype
        :type releasetype: str - :data:`jukeboxcore.djadapter.RELEASETYPES`
        :param typ: the file type, see :data:`TYPES`
        :type typ: str
        :param descriptor: the descriptor, if the taskfile has one.
        :type descriptor: str|None
        :raises: None
        """
        super(TaskFileInfo, self).__init__()
        self.task = task
        self.version = version
        self.releasetype = releasetype
        self.descriptor = descriptor
        self.typ = typ

    @classmethod
    def get_latest(cls, task, releasetype, typ, descriptor=None):
        """Returns a TaskFileInfo that with the latest existing version and the provided info

        :param task: the task of the taskfile
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :param releasetype: the releasetype
        :type releasetype: str - :data:`jukeboxcore.djadapter.RELEASETYPES`
        :param typ: the file type, see :data:`TYPES`
        :type typ: str
        :param descriptor: the descriptor, if the taskfile has one.
        :type descriptor: str|None
        :returns: taskfileinfoobject with the latest extisting version and the provided info
                  or none if there is no latest.
        :rtype: :class:`TaskFileInfo` | None
        :raises: None
        """
        qs = dj.taskfiles.filter(task=task, releasetype=releasetype, descriptor=descriptor, typ=typ)
        if qs.exists():
            maxver = qs.aggregate(Max('version'))['version__max']
            return TaskFileInfo(task, maxver, releasetype, typ, descriptor)
        else:
            return

    @classmethod
    def get_next(cls, task, releasetype, typ, descriptor=None):
        """Returns a TaskFileInfo that with the next available version and the provided info

        :param task: the task of the taskfile
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :param releasetype: the releasetype
        :type releasetype: str - :data:`jukeboxcore.djadapter.RELEASETYPES`
        :param typ: the file type, see :data:`TYPES`
        :type typ: str
        :param descriptor: the descriptor, if the taskfile has one.
        :type descriptor: str|None
        :returns: taskfileinfoobject with next available version and the provided info
        :rtype: :class:`TaskFileInfo`
        :raises: None
        """
        qs = dj.taskfiles.filter(task=task, releasetype=releasetype, descriptor=descriptor, typ=typ)
        if qs.exists():
            ver = qs.aggregate(Max('version'))['version__max']+1
        else:
            ver = 1
        return TaskFileInfo(task=task, version=ver, releasetype=releasetype, typ=typ, descriptor=descriptor)


class JB_File(object):
    """This class generates filenames for arbitrary objects

    The object should contain all the information that is needed for
    constructing a distinct filepath. It should be a subclass of :class:`FileInfo`.
    This class uses a list of :class:`FileElement` to generate the filepath.
    Each element should know how to handle the object. So only use certain objects with certain elements.
    Each element contributes to either the path or the name or both.
    The JB_File has a dictionary :data:`JB_File.ELEMENTPRESETS` that have a list of element
    for every :class:`FileInfo` sublcass.
    """

    ELEMENTPRESETS = {
        TaskFileInfo: [AttrElement('task.project.path', 'task.project.short'),
                       StaticElement("production"),
                       SoftwareElement(),
                       TaskGroupElement(),
                       AttrElement('task.element.name', 'task.element.name'),
                       AttrElement('task.department.name', 'task.department.short'),
                       AttrElement('releasetype'),
                       AttrElement(None, 'descriptor'),
                       AttrElement(None, 'version', None, 'v%03i')]
    }
    """this dict has a list of elements for each file info type"""
    EXTENSIONS = {
        TaskFileInfo: TaskFileExtElement()
    }
    """this dict has extensionelement for each file info type"""

    def __init__(self, obj):
        """Constructs a new JB_File. the type of object determines the elementspreset (the generation of the path).

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :raises: None
        """
        self._obj = obj
        try:
            self._elements = self.ELEMENTPRESETS[obj.__class__]
        except KeyError:
            typename = obj.__class__.__name__
            supported = [x.__name__ for x in self.ELEMENTPRESETS.keys()]
            raise TypeError("JB_File does not know how to handle the fileinfo. FileInfo is of type %s, supported are: %s" % (typename, supported))
        try:
            self._extel = self.EXTENSIONS[obj.__class__]
        except KeyError:
            typename = obj.__class__.__name__
            supported = [x.__name__ for x in self.EXTENSIONS.keys()]
            raise TypeError("JB_File does not know how to handle the fileinfo to get an extension. FileInfo is of type %s, supported are: %s" % (typename, supported))

    def get_ext(self, obj=None):
        """Return the file extension

        :param obj: the fileinfo with information. If None, this will use the stored object of JB_File
        :type obj: :class:`FileInfo`
        :returns: the file extension
        :rtype: str
        :raises: None
        """
        if obj is None:
            obj = self._obj
        return self._extel.get_ext(obj)

    def get_path(self, obj=None):
        """Return the path (excluding the filename)

        :param obj: the fileinfo with information. If None, this will use the stored object of JB_File
        :type obj: :class:`FileInfo`
        :returns: the path to the file
        :rtype: str
        :raises: None
        """
        if obj is None:
            obj = self._obj
        chunks = []
        for e in self._elements:
            d = e.get_dir(obj)
            if d is not None:
                chunks.append(d)
        path = os.path.join(*chunks)
        return os.path.normpath(path)

    def get_name(self, obj=None, withext=True):
        """Return the filename

        :param obj: the fileinfo with information. If None, this will use the stored object of JB_File
        :type obj: :class:`FileInfo`
        :param withext: If True, return with the fileextension.
        :type withext: bool
        :returns: the filename, default is with fileextension
        :rtype: str
        :raises: None
        """
        if obj is None:
            obj = self._obj
        chunks = []
        for e in self._elements:
            c = e.get_chunk(obj)
            if c is not None:
                chunks.append(c)
        name = '_'.join(chunks)
        if withext:
            name = os.extsep.join([name, self.get_ext(obj)])
        return name

    def get_fullpath(self, withext=True):
        """Return the filepath with the filename

        :param withext: If True, return with the fileextension.
        :type withext: bool
        :returns: None
        :rtype: None
        :raises: None
        """
        p = self.get_path(self._obj)
        n = self.get_name(self._obj, withext)
        fp = os.path.join(p,n)
        return os.path.normpath(fp)

    def get_obj(self, ):
        """Return the object that contains the information

        :returns: the object with information
        :rtype: :class:`FileInfo`
        :raises: None
        """
        return self._obj

    def set_obj(self, obj):
        """Set the object that contains the information

        :param obj: the fileinfo with information.
        :type obj: :class:`FileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        self._obj = obj

    def get_elements(self, ):
        """Return the file elements

        :returns: list with FileElements that are used to generate the filepath
        :rtype: list of :class:`FileElement`
        :raises: None
        """
        return self._elements

    def create_directory(self, path=None):
        """Create the directory for the given path. If path is None use the path of this instance

        :param path: the path to create
        :type path: str
        :returns: None
        :rtype: None
        :raises: OSError
        """
        if path is None:
            path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
