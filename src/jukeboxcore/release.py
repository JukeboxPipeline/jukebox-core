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

    def relase(self, ):
        """Create a release

        Perform Sanity checks on work file.
        Copy work file to releasefile location.
        Perform cleanup actions on releasefile.

        :returns: None
        :rtype: None
        :raises: None
        """
        result = self.sanity_check(self._workfile)
        if not result.passed():
            if not self.confirm_check_result(result):
                return
        self.copy_file(self._workfile, self._releasefile)
        self.create_db_entry(self._releasefile)
        self.cleanup(self._releasefile)

    def sanity_check(self, f):
        """Check the given JB_File object

        :param f: the file to check
        :type f: :class:`JB_File`
        :returns: a check result object
        :rtype: :class:`CheckResult``
        :raises: None
        """
        pass

    def confirm_check_result(self, result):
        """Display the result to the user and ask for confirmation if you can continue

        :param result: the result of the sanity check
        :type result: :class:`CheckResult`
        :returns: None
        :rtype: None
        :raises: None
        """
        r = result.show_confirm_dialog()
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
