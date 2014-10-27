"""Module for releasing workfiles.

The release process in general works like this:

  1. Sanity checks
  2. Copy the file to release location and create db entry
  3. Open the release file and perform cleanup actions

Step 2. is the same for every file. Only 1. and 3. vary
"""
import os
import shutil

from jukeboxcore.djadapter import RELEASETYPES
from jukeboxcore.filesys import TaskFileInfo, JB_File


class Release(object):
    """Handle file releases of taskfiles
    """

    def __init__(self, taskfileinfo):
        """Create a release object that can handle the release of the given taskfileinfo

        :param taskfileinfo: the taskfileinfo for the file that should be released
        :type taskfileinfo: :class:`TaskFileInfo`
        :raises: None
        """
        super(Release, self).__init__()
        self._tfi = taskfileinfo
        self._rfi = TaskFileInfo.get_next(self._tfi.task,
                                          RELEASETYPES['release'],
                                          self._tfi.typ,
                                          self._tfi.descriptor)
        self._workfile = JB_File(self._tfi)
        self._releasefile = JB_File(self._rfi)

    def release(self, checks, cleanup, force=False):
        """Create a release

        Perform Sanity checks on work file.
        Copy work file to releasefile location.
        Perform cleanup actions on releasefile.

        :param checks: the file action object that holds the checks to perform
        :type checks: :class:`FileAction`
        :param force: If True, does not perform sanity checks.
        :type force: bool
        :param cleanup: The file action object that holds actions to perform on the released file
        :type cleanup: :class:`FileAction`
        :returns: None
        :rtype: None
        :raises: None
        """
        if not force:
            self.sanity_check(self._workfile, checks)
            if not checks.passed():
                if not self.confirm_check_result(checks):
                    return
        self.copy_file(self._workfile, self._releasefile)
        self.create_db_entry(self._releasefile)
        self.cleanup(self._releasefile, cleanup)

    def sanity_check(self, f, checks):
        """Check the given JB_File object

        :param f: the file to check
        :type f: :class:`JB_File`
        :param checks: the file action object with sanity checks
        :type checks: :class:`FileAction`
        :returns: a check result object
        :rtype: :class:`CheckResult``
        :raises: None
        """
        pass

    def confirm_check_result(self, checks):
        """Display the result to the user and ask for confirmation if you can continue

        :param checks: the file action object that has been already processed.
        :type checks: :class:`FileAction`
        :returns: None
        :rtype: None
        :raises: None
        """
        r = checks.show_confirm_dialog()
        return r

    def copy_file(self, old, new):
        """Copy the old file to the location of the new file

        :param old: The file to copy
        :type old: :class:`JB_File`
        :param new: The JB_File for the new location
        :type new: :class:`JB_File`
        :returns: None
        :rtype: None
        :raises: None
        """
        oldp = old.get_fullpath()
        newp = new.get_fullpath()
        newdir = os.path.dirname(newp)
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        shutil.copy(oldp, newp)

    def create_db_entry(self, f, comment):
        """Create a db entry for the given file

        :param f: the file to create a db entry for
        :type f: :class:`JB_File`
        :param comment: comment for the release
        :type comment: :class:`str`
        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def cleanup(self, f, cleanup):
        """Cleanup the given releasefile

        :param f: the releasefile to cleanup
        :type f: :class:`JB_File`
        :param cleanup: a file action object that holds cleanup actions for the given file
        :type cleanup: :class:`FileAction`
        :returns: None
        :rtype: None
        :raises: None
        """
        pass
