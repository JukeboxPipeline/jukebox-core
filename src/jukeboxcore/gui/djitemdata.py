"""This module holds :class:`jukeboxcore.gui.treemodel.ItemData` subclasses that represent data in our database, e.g. a Project, Sequence etc"""
from PySide import QtCore

from jukeboxcore.gui.main import dt_to_qdatetime
from jukeboxcore.gui.treemodel import ItemData


def prj_name_data(project, role):
    """Return the data for name

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.name


def prj_short_data(project, role):
    """Return the data for short

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the short
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.short


def prj_path_data(project, role):
    """Return the data for path

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the path
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.path


def prj_created_data(project, role):
    """Return the data for created

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the created
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.date_created.isoformat(' ')


def prj_semester_data(project, role):
    """Return the data for semester

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the semester
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.semester


def prj_fps_data(project, role):
    """Return the data for fps

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the fps
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return str(project.framerate)


def prj_resolution_data(project, role):
    """Return the data for resolution

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the resolution
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return '%s x %s' % (project.resx, project.resy)


def prj_scale_data(project, role):
    """Return the data for scale

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the scale
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.scale


def prj_status_data(project, role):
    """Return the data for status

    :param project: the project that holds the data
    :type project: :class:`jukeboxcore.djadapter.models.Project`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the status
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return project.status


class ProjectItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a project
    """

    def __init__(self, project):
        """Constructs a new item data for the project

        :param project: the project to represent
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :raises: None
        """
        super(ProjectItemData, self).__init__()
        self._project = project

    columns = [prj_name_data,
               prj_short_data,
               prj_path_data,
               prj_created_data,
               prj_semester_data,
               prj_status_data,
               prj_resolution_data,
               prj_fps_data,
               prj_scale_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._project, role)

    def internal_data(self, ):
        """Return the project

        :returns: the project
        :rtype: :class:`jukeboxcore.djadapter.models.Project`
        :raises: None
        """
        return self._project


def seq_name_data(seq, role):
    """Return the data for name

    :param seq: the sequence that holds the data
    :type seq: :class:`jukeboxcore.djadapter.models.Sequence`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return seq.name


def seq_description_data(seq, role):
    """Return the data for description

    :param seq: the sequence that holds the data
    :type seq: :class:`jukeboxcore.djadapter.models.Sequence`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the description
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return seq.description


class SequenceItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a sequence
    """

    def __init__(self, sequence):
        """Constructs a new item data for the sequence

        :param sequence: the sequence to represent
        :type sequence: :class:`jukeboxcore.djadapter.models.Sequence`
        :raises: None
        """
        super(SequenceItemData, self).__init__()
        self._sequence = sequence

    columns = [seq_name_data,
               seq_description_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._sequence, role)

    def internal_data(self, ):
        """Return the sequence

        :returns: the sequence
        :rtype: :class:`jukeboxcore.djadapter.models.Sequence`
        :raises: None
        """
        return self._sequence


def shot_name_data(shot, role):
    """Return the data for name

    :param shot: the shot that holds the data
    :type shot: :class:`jukeboxcore.djadapter.models.Shot`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return shot.name


def shot_description_data(shot, role):
    """Return the data for description

    :param shot: the shot that holds the data
    :type shot: :class:`jukeboxcore.djadapter.models.Shot`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the description
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return shot.description


def shot_duration_data(shot, role):
    """Return the data for duration

    :param shot: the shot that holds the data
    :type shot: :class:`jukeboxcore.djadapter.models.Shot`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the duration
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return str(shot.duration)


def shot_start_data(shot, role):
    """Return the data for startframe

    :param shot: the shot that holds the data
    :type shot: :class:`jukeboxcore.djadapter.models.Shot`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the start
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return str(shot.startframe)


def shot_end_data(shot, role):
    """Return the data for endframe

    :param shot: the shot that holds the data
    :type shot: :class:`jukeboxcore.djadapter.models.Shot`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the end
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return str(shot.endframe)


class ShotItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a shot
    """

    def __init__(self, shot):
        """Constructs a new item data for the shot

        :param shot: the shot to represent
        :type shot: :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        super(ShotItemData, self).__init__()
        self._shot = shot

    columns = [shot_name_data,
               shot_description_data,
               shot_duration_data,
               shot_start_data,
               shot_end_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._shot, role)

    def internal_data(self, ):
        """Return the shot

        :returns: the shot
        :rtype: :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        return self._shot


def task_name_data(task, role):
    """Return the data for name

    :param task: the task that holds the data
    :type task: :class:`jukeboxcore.djadapter.models.Task`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return task.name


def task_short_data(task, role):
    """Return the data for short name

    :param task: the task that holds the data
    :type task: :class:`jukeboxcore.djadapter.models.Task`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the short name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return task.short


class TaskItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a task
    """

    def __init__(self, task):
        """Constructs a new item data for the task

        :param task: the task to represent
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :raises: None
        """
        super(TaskItemData, self).__init__()
        self._task = task

    columns = [task_name_data,
               task_short_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._task, role)

    def internal_data(self, ):
        """Return the task

        :returns: the task
        :rtype: :class:`jukeboxcore.djadapter.models.Task`
        :raises: None
        """
        return self._task


def taskfile_path_data(file_, role):
    """Return the data for path

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the path
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return file_.path


def taskfile_user_data(file_, role):
    """Return the data for user

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the user
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return file_.user.username


def taskfile_created_data(file_, role):
    """Return the data for created date

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the created date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        dt = file_.date_created
        return dt_to_qdatetime(dt)


def taskfile_updated_data(file_, role):
    """Return the data for updated date

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the updated date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        dt = file_.date_updated
        return dt_to_qdatetime(dt)


def taskfile_version_data(file_, role):
    """Return the data for version

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the version
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return 'v%03i' % file_.version


def taskfile_rtype_data(file_, role):
    """Return the data for rtype

    :param file_: the file that holds the data
    :type file_: :class:`jukeboxcore.djadapter.models.File`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the releasetype
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return file_.releasetype


class TaskFileItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents a taskfile
    """

    def __init__(self, taskfile):
        """Constructs a new item data for the taskfile

        :param taskfile: the taskfile to represent
        :type taskfile: :class:`jukeboxcore.djadapter.models.TaskFile`
        :raises: None
        """
        super(TaskFileItemData, self).__init__()
        self._taskfile = taskfile

    columns = [taskfile_version_data,
               taskfile_rtype_data,
               taskfile_path_data,
               taskfile_user_data,
               taskfile_created_data,
               taskfile_updated_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._taskfile, role)

    def internal_data(self, ):
        """Return the taskfile

        :returns: the taskfile
        :rtype: :class:`jukeboxcore.djadapter.models.TaskFile`
        :raises: None
        """
        return self._taskfile


def atype_name_data(atype, role):
    """Return the data for name

    :param atype: the assettype that holds the data
    :type atype: :class:`jukeboxcore.djadapter.models.Atype`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return atype.name


def atype_description_data(atype, role):
    """Return the data for description

    :param atype: the assettype that holds the data
    :type atype: :class:`jukeboxcore.djadapter.models.Atype`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the description
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return atype.description


class AtypeItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents an assettype
    """

    def __init__(self, atype):
        """Constructs a new item data for the assettype

        :param atype: the assettype to represent
        :type atype: :class:`jukeboxcore.djadapter.models.Atype`
        :raises: None
        """
        super(AtypeItemData, self).__init__()
        self._atype = atype

    columns = [atype_name_data,
               atype_description_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._atype, role)

    def internal_data(self, ):
        """Return the assettype

        :returns: the shot
        :rtype: :class:`jukeboxcore.djadapter.models.Atype`
        :raises: None
        """
        return self._atype


def asset_name_data(asset, role):
    """Return the data for name

    :param asset: the asset that holds the data
    :type asset: :class:`jukeboxcore.djadapter.models.Asset`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the name
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return asset.name


def asset_description_data(asset, role):
    """Return the data for description

    :param asset: the asset that holds the data
    :type asset: :class:`jukeboxcore.djadapter.models.Asset`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the description
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole:
        return asset.description


class AssetItemData(ItemData):
    """Item Data for :class:`jukeboxcore.gui.treemodel.TreeItem` that represents an asset
    """

    def __init__(self, asset):
        """Constructs a new item data for the asset

        :param asset: the asset to represent
        :type asset: :class:`jukeboxcore.djadapter.models.Asset`
        :raises: None
        """
        super(AssetItemData, self).__init__()
        self._asset = asset

    columns = [asset_name_data,
               asset_description_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._asset, role)

    def internal_data(self, ):
        """Return the asset

        :returns: the asset
        :rtype: :class:`jukeboxcore.djadapter.models.Asset`
        :raises: None
        """
        return self._asset


def note_content_data(note, role):
    """Return the data for content

    :param note: the note that holds the data
    :type note: :class:`jukeboxcore.djadapter.models.Note`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the created date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return note.content


def note_user_data(note, role):
    """Return the data for user

    :param note: the note that holds the data
    :type note: :class:`jukeboxcore.djadapter.models.Note`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the created date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        return note.user.username


def note_created_data(note, role):
    """Return the data for created date

    :param note: the note that holds the data
    :type note: :class:`jukeboxcore.djadapter.models.Note`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the created date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        dt = note.date_created
        return dt_to_qdatetime(dt)


def note_updated_data(note, role):
    """Return the data for updated date

    :param note: the note that holds the data
    :type note: :class:`jukeboxcore.djadapter.models.Note`
    :param role: item data role
    :type role: QtCore.Qt.ItemDataRole
    :returns: data for the updated date
    :rtype: depending on role
    :raises: None
    """
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
        dt = note.date_updated
        return dt_to_qdatetime(dt)


class NoteItemData(ItemData):
    """Item data for :class:`jukeboxcore.gui.treemodel.TreeITem` that represents a note.
    """

    def __init__(self, note):
        """Constructs a new item data for the note

        :param note: the note to represent
        :type note: :class:`jukeboxcore.djadapter.models.Note`
        :raises: None
        """
        super(NoteItemData, self).__init__()
        self._note = note

    columns = [note_content_data,
               note_user_data,
               note_created_data,
               note_updated_data]

    def column_count(self, ):
        """Return the number of columns that can be queried for data

        :returns: the number of columns
        :rtype: int
        :raises: None
        """
        return len(self.columns)

    def data(self, column, role):
        """Return the data for the specified column and role

        The column addresses one attribute of the data.

        :param column: the data column
        :type column: int
        :param role: the data role
        :type role: QtCore.Qt.ItemDataRole
        :returns: data depending on the role
        :rtype:
        :raises: None
        """
        return self.columns[column](self._note, role)

    def internal_data(self, ):
        """Return the note

        :returns: the note
        :rtype: :class:`jukeboxcore.djadapter.models.Note`
        :raises: None
        """
        return self._note

    def flags(self, ):
        """Return the item flags for the item

        This returns editable True to enable custom editors.

        :returns: the item flags
        :rtype: QtCore.Qt.ItemFlags
        :raises: None
        """
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
