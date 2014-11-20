"""Module for releasing workfiles.

The release process in general works like this:

  1. Open the work file and run sanity checks
  2. Copy the file to release location and create db entry
  3. Open the release file and perform cleanup actions

Step 2. is the same for every file. Only 1. and 3. vary
"""
import abc

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore.djadapter import RELEASETYPES
from jukeboxcore.filesys import TaskFileInfo, JB_File, copy_file, delete_file
from jukeboxcore.action import ActionStatus, ActionUnit, ActionCollection
from jukeboxcore.gui.widgets.actionreportdialog import ActionReportDialog


class Release(object):
    """Handle file releases of taskfiles
    """

    def __init__(self, taskfileinfo, checks, cleanup, comment):
        """Create a release object that can handle the release of the given taskfileinfo

        :param taskfileinfo: the taskfileinfo for the file that should be released
        :type taskfileinfo: :class:`TaskFileInfo`
        :param checks: the action collection object that holds the checks to perform.
                       It should accept a :class:`JB_File` as object for execute.
        :type checks: :class:`ActionCollection`
        :param cleanup: The action collection object that holds actions to perform on the released file.
                        It should accept a :class:`JB_File` as object for execute.
        :type cleanup: :class:`ActionCollection`
        :param comment: The comment for the release
        :type comment:
        :raises: None
        """
        super(Release, self).__init__()
        self._tfi = taskfileinfo
        self._rfi = TaskFileInfo.get_next(self._tfi.task,
                                          RELEASETYPES['release'],
                                          self._tfi.typ,
                                          None)
        self._workfile = JB_File(self._tfi)
        self._releasefile = JB_File(self._rfi)
        self._checks = checks
        self._cleanup = cleanup
        self.comment = comment
        self._releasedbentry = None
        self._commentdbentry = None

    def release(self):
        """Create a release

        1. Perform Sanity checks on work file.
        2. Copy work file to releasefile location.
        3. Perform cleanup actions on releasefile.

        :returns: True if successfull, False if not.
        :rtype: bool
        :raises: None
        """
        log.info("Releasing: %s", self._workfile.get_fullpath())
        ac = self.build_actions()
        ac.execute(self)
        s = ac.status().value
        if not s == ActionStatus.SUCCESS:
            ard = ActionReportDialog(ac)
            ard.exec_()
            pass
        return s == ActionStatus.SUCCESS

    def build_actions(self):
        """Create an ActionCollection that will perform sanity checks, copy the file,
        create a database entry and perform cleanup actions and in case of a failure clean everything up.

        :param work: the workfile
        :type work: :class:`JB_File`
        :param release: the releasefile
        :type release: :class:`JB_File`
        :param checks: the action collection object with sanity checks
                       It should accept a :class:`JB_File` as object for execute.
        :type checks: :class:`ActionCollection`
        :param cleanup: a action collection object that holds cleanup actions for the given file.
                        It should accept a :class:`JB_File` as object for execute.
        :type cleanup: :class:`ActionCollection`
        :param comment: comment for the release
        :type comment: :class:`str`
        :returns: An ActionCollection ready to execute.
        :rtype: :class:`ActionCollection`
        :raises: None
        """
        checkau = ActionUnit("Sanity Checks",
                             "Check the workfile. If the file is not conform, ask the user to continue.",
                             self.sanity_check)
        copyau = ActionUnit("Copy File",
                            "Copy the workfile to the releasefile location.",
                            self.copy,
                            depsuccess=[checkau])
        dbau = ActionUnit("Create DB entry",
                          "Create an entry in the database for the releasefile",
                          self.create_db_entry,
                          depsuccess=[copyau])
        cleanau = ActionUnit("Cleanup",
                             "Cleanup the releasefile. If something fails, ask the user to continue.",
                             self.cleanup,
                             depsuccess=[dbau])
        deletefau1 = ActionUnit("Delete the releasefile.",
                                "In case the db entry creation fails, delete the releasefile.",
                                self.delete_releasefile,
                                depfail=[dbau])
        deletefau2 = ActionUnit("Delete the releasefile.",
                                "In case the cleanup fails, delete the releasefile.",
                                self.delete_releasefile,
                                depsuccess=[copyau],
                                depfail=[cleanau])
        deletedbau = ActionUnit("Delete the database entry.",
                                "In case the cleanup fails, delete the database entry",
                                self.delete_db_entry,
                                depsuccess=[dbau],
                                depfail=[cleanau])
        return ActionCollection([checkau, copyau, dbau, cleanau, deletefau1, deletefau2, deletedbau])

    def sanity_check(self, release):
        """Perform sanity checks on the workfile of the given release

        This is inteded to be used in a action unit.

        :param release: the release with the workfile and sanity checks
        :type release: :class:`Release`
        :returns: the action status of the sanity checks
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        log.info("Performing sanity checks.")
        return execute_actioncollection(release._workfile, actioncollection=release._checks, confirm=True)

    def copy(self, release):
        """Copy the workfile of the given release to the releasefile location

        This is inteded to be used in a action unit.

        :param release: the release with the release and workfile
        :type release: :class:`Release`
        :returns: an action status
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        workfp = release._workfile.get_fullpath()
        releasefp = release._releasefile.get_fullpath()
        copy_file(release._workfile, release._releasefile)
        return ActionStatus(ActionStatus.SUCCESS,
                            msg="Copied %s to %s location." % (workfp,
                                                               releasefp))

    def create_db_entry(self, release):
        """Create a db entry for releasefile of the given release

        Set _releasedbentry and _commentdbentry of the given release file

        This is inteded to be used in a action unit.

        :param release: the release with the releasefile and comment
        :type release: :class:`Release`
        :returns: an action status
        :rtype: :class:`ActionStatus`
        :raises: ValidationError, If the comment could not be created, the TaskFile is deleted and the Exception is propagated.
        """
        log.info("Create database entry with comment: %s", release.comment)
        tfi = release._releasefile.get_obj()
        tf, note = tfi.create_db_entry(release.comment)
        release._releasedbentry = tf
        release._commentdbentry = note
        return ActionStatus(ActionStatus.SUCCESS,
                            msg="Created database entry for the release filw with comment: %s" % release.comment)

    def cleanup(self, release):
        """Perform cleanup actions on the releasefile of the given release

        This is inteded to be used in a action unit.

        :param release: the release with the releasefile and cleanup actions
        :type release: :class:`Release`
        :returns: the action status of the cleanup actions
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        log.info("Performing cleanup.")
        return execute_actioncollection(release._releasefile, actioncollection=release._cleanup, confirm=True)

    def delete_releasefile(self, release):
        """Delete the releasefile of the given release

        This is inteded to be used in a action unit.

        :param release: the release with the releasefile
        :type release: :class:`Release`
        :returns: an action status
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        fp = release._releasefile.get_fullpath()
        log.info("Deleting release file %s", fp)
        delete_file(release._releasefile)
        return ActionStatus(ActionStatus.SUCCESS,
                            msg="Deleted %s" % fp)

    def delete_db_entry(self, release):
        """Delete the db entries for releasefile and comment of the given release

        :param release: the release with the releasefile and comment db entries
        :type release: :class:`Release`
        :returns: an action status
        :rtype: :class:`ActionStatus`
        :raises: None
        """
        log.info("Delete database entry for file.")
        release._releasedbentry.delete()
        log.info("Delete database entry for comment.")
        release._commentdbentry.delete()
        return ActionStatus(ActionStatus.SUCCESS,
                            msg="Deleted database entries for releasefile and comment")


class ReleaseActions(object):
    """Abstract class that provides sanity checks and cleanups for a release

    This class can also offer a widget to a :class:`jukeboxcore.gui.widgets.releasewin.ReleaseWin`
    to give the user options. Depending on these options it should return sanity checks and cleanup
    actions.

    Subclass it and implement, :meth:`ReleaseActions.get_checks` and :meth:`ReleaseActions.get_cleanups`.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new releae option widget

        :raises: None
        """
        super(ReleaseActions, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def get_checks(self, ):
        """Get the sanity check actions for a releaes depending on the selected options

        :returns: the cleanup actions
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        pass

    @abc.abstractmethod
    def get_cleanups(self, ):
        """Get the cleanup actions for a releaes depending on the selected options

        :returns: the cleanup actions
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        pass

    @abc.abstractmethod
    def option_widget(self, ):
        """Return a widget that gives the user options for the release.

        .. Note:: The widget might get parented to another window. So create a new
                  ReleaseAction instance for each window.

        The cleanups and sanity checks should correspond to the options the user
        selects in this widget.

        :returns: a widget with options for the user
        :rtype: :class:`PySide.QtGui.QWidget` | None
        :raises: None
        """
        pass


def execute_actioncollection(obj, actioncollection, confirm=True):
    """Execute the given actioncollection with the given object

    :param obj: the object to be processed
    :param actioncollection:
    :type actioncollection: :class:`ActionCollection`
    :param confirm: If True, ask the user to continue, if actions failed.
    :type confirm: :class:`bool`
    :returns: An action status. If the execution fails but the user confirms, the status will be successful.
    :rtype: :class:`ActionStatus`
    :raises: None
    """
    actioncollection.execute(obj)
    status = actioncollection.status()
    if status.value == ActionStatus.SUCCESS or not confirm:
        return status
    ard = ActionReportDialog(actioncollection)
    confirmed = ard.exec_()
    if confirmed:
        msg = "User confirmed to continue although the status was: %s" % status.message,
        s = ActionStatus.SUCCESS
        tb = status.traceback
    else:
        s = status.value
        msg = "User aborted the actions because the status was: %s" % status.message,
        tb = status.traceback
    return ActionStatus(s, msg, tb)
