"""Module for releasing workfiles.

The release process in general works like this:

  1. Open the work file and run sanity checks
  2. Copy the file to release location and create db entry
  3. Open the release file and perform cleanup actions

Step 2. is the same for every file. Only 1. and 3. vary
"""
import os
import tempfile
import subprocess

import yaml

from jukeboxcore.djadapter import RELEASETYPES
from jukeboxcore.filesys import TaskFileInfo, JB_File, copy_file, delete_file
from jukeboxcore.action import ActionStatus


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
                                          self._tfi.descriptor)
        self._workfile = JB_File(self._tfi)
        self._releasefile = JB_File(self._rfi)
        self.checks = checks
        self.cleanup = cleanup
        self.comment = comment

    def release(self):
        """Create a release

        The release is executed in another subprocess.
        So first we dump this release file for the subprocess.
        In the process these steps are executed:

          1. Load the dumped release
          2. Start the release process.
             In the process, do:

             1. Load dumped release, see :func:`load_release`
             2. Execute the release actions, see :func:`run_release`:

               1. Perform Sanity checks on work file.
               2. Copy work file to releasefile location.
               3. Perform cleanup actions on releasefile.

        :returns: the subprocess that handles the release
        :rtype: :class:`subprocess.Popen`
        :raises: None
        """
        f = self.dump_release()
        return self.start_release_process(f.name)

    def execute_actions(self, ):
        """Execute the sanity checks, copy the release file and perform the cleanup

        :returns: None
        :rtype: None
        :raises: None
        """
        self.sanity_check(self._workfile, self.checks)
        if not self.checks.status().value == ActionStatus.SUCCESS:
            if not self.confirm_check_result(self.checks):
                return
        copy_file(self._workfile, self._releasefile)
        self.cleanup(self._releasefile, self.cleanup)
        if not self.cleanup.status().value == ActionStatus.SUCCESS:
            if not self.confirm_check_result(self.cleanup):
                delete_file(self._releasefile)
                return
        self.create_db_entry(self._releasefile, self.comment)

    def dump_release(self):
        """Dump this release object into a temporary file and return it

        The temp file will not be deleted when closed.
        You can open it in a subprocess but see :func:`load_release`
        for how to do that.

        :returns: a temporary file object
        :rtype: :class:`tempfile.NamedTemporaryFile`
        :raises: None
        """
        # delete False is important so the subprocess can still read it
        with tempfile.NamedTemporaryFile(delete=False) as f:
            yaml.dump(self, f)
        return f

    def start_release_process(self, dump):
        """Start a subprocess that executes the given, dumped release

        :param dump: The path to the dumped release (with :meth:`Release.dump_release`) file.
        :type dump: :class:`str`
        :returns: the created subprocess
        :rtype: :class:`subprocess.Popen`
        :raises: None
        """
        args = ['jukebox', 'release', dump]
        return subprocess.Popen(args)

    def sanity_check(self, f, checks):
        """Check the given JB_File object

        :param f: the file to check
        :type f: :class:`JB_File`
        :param checks: the action collection object with sanity checks
                       It should accept a :class:`JB_File` as object for execute.
        :type checks: :class:`ActionCollection`
        :returns: None
        :rtype: None
        :raises: None
        """
        checks.execute(f)

    def confirm_check_result(self, checks):
        """Display the result to the user and ask for confirmation if you can continue

        :param checks: the action collection object that has been already processed.
                       It should accept a :class:`JB_File` as object for execute.
        :type checks: :class:`ActionCollection`
        :returns: True, if the user confirmed to continue. False if the user wants to abort.
        :rtype: :class:`bool`
        :raises: None
        """
        raise NotImplementedError

    def create_db_entry(self, f, comment):
        """Create a db entry for the given file

        :param f: the file to create a db entry for
        :type f: :class:`JB_File`
        :param comment: comment for the release
        :type comment: :class:`str`
        :returns: The created TaskFile django instance and the comment. If the comment was empty, None is returned instead
        :rtype: tuple of :class:`dj.models.TaskFile` and :class:`dj.models.Note`|None
        :raises: ValidationError, If the comment could not be created, the TaskFile is deleted and the Exception is propagated.
        """
        tfi = f.get_obj()
        return tfi.create_db_entry(comment)

    def cleanup(self, f, cleanup):
        """Cleanup the given releasefile

        :param f: the releasefile to cleanup
        :type f: :class:`JB_File`
        :param cleanup: a action collection object that holds cleanup actions for the given file.
                        It should accept a :class:`JB_File` as object for execute.
        :type cleanup: :class:`ActionCollection`
        :returns: None
        :rtype: None
        :raises: None
        """
        cleanup.execute(f)


def load_release(dump):
    """Load the given, dumped release and return the :class:`Release` instance

    Raises an TypeError, if the loaded object is no :class:`Release` instance.

    The file is opened like this::

      os.fdopen(os.open(dump, os.O_RDWR | os.O_BINARY | os.O_TEMPORARY), 'rb')

    This ensures that a temporary file on windows can be opened multiple times.
    I found the solution here: http://stackoverflow.com/a/15235559
    The os.O_TEMPORARY is the key.

    :param dump: The path to the dumped release (with :meth:`Release.dump_release`) file.
    :type dump: :class:`str`
    :returns: the loaded release
    :rtype: :class:`Release`
    :raises: AssertionError
    """
    r = None
    f = os.fdopen(os.open(dump, os.O_RDWR | os.O_BINARY | os.O_TEMPORARY), 'rb')
    r = yaml.load(f)
    f.close()
    if not isinstance(r, Release):
        raise TypeError("Expected to load a release instance. Instead got: %s" % r)
    return r


def run_release(dump):
    """Load the given, dumped release and execute the release actions

    This funtion is intended to be run in a subprocess, when using
    :meth:`Release.start_release_process`.
    Executes :meth:`Releaes.execute_actions` of the loaded :class:`Release` instance.

    :param dump: The path to the dumped release (with :meth:`Release.dump_release`) file.
    :type dump: :class:`str`
    :returns: None
    :rtype: None
    :raises: None
    """
    release = load_release(dump)
    release.execute_actions()
