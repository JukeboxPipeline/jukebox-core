from PySide import QtCore

from jukeboxcore.filesys import TaskFileInfo, JB_File


class JukeboxSignals(QtCore.QObject):
    """Collection of global signals.

    Use :meth:`JukeboxSignals.get` to get an instance.
    Then connect to signals::

       from jukeboxcore import signals 

       def open_shot_callback(taskfileinfo):
           print "Opening", taskfileinfo
           print "Task", taskfileinfo.task.name
           print "version", taskfileinfo.version
           print "releasytype", taskfileinfo.releasetype

       js = signals.JukeboxSignals.get()
       js.open_shot.connect(open_shot_callback)
    """

    _instance = None
    """The global instance"""
    
    before_open_shot = QtCore.QSignal(TaskFileInfo)
    """Signal gets emitted right before a shot gets opened.
    Arguments: :class:`TaskFileInfo`"""
    after_open_shot = QtCore.QSignal(TaskFileInfo)
    """Signal gets emitted right after a shot gets opened.
    Arguments: :class:`TaskFileInfo`"""
    before_open_asset = QtCore.QSignal(TaskFileInfo)
    """Signal gets emitted right before a asset gets opened.
    Arguments: :class:`TaskFileInfo`"""
    after_open_asset = QtCore.QSignal(TaskFileInfo)
    """Signal gets emitted right after a asset gets opened.
    Arguments: :class:`TaskFileInfo`"""

    before_save_shot = QtCore.QSignal(JB_File, TaskFileInfo)
    """Signal gets emitted right before a shot gets saved.
    Arguments: :class:`JB_File`, :class:`TaskFileInfo`"""
    after_save_shot = QtCore.QSignal(JB_File, TaskFileInfo)
    """Signal gets emitted right after a shot gets saved.
    Arguments: :class:`JB_File`, :class:`TaskFileInfo`"""
    before_save_asset = QtCore.QSignal(JB_File, TaskFileInfo)
    """Signal gets emitted right before a asset gets saved.
    Arguments: :class:`JB_File`, :class:`TaskFileInfo`"""
    after_save_asset = QtCore.QSignal(JB_File, TaskFileInfo)
    """Signal gets emitted right after a asset gets saved.
    Arguments: :class:`JB_File`, :class:`TaskFileInfo`"""

    @classmethod
    def get(cls):
        """Always return the same instance of :class:`JukeboxSignals`.

        Create instance if it does not exist.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
