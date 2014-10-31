import os

import pytest

from jukeboxcore import release
from jukeboxcore.filesys import TaskFileInfo, JB_File
from jukeboxcore.action import ActionUnit, ActionCollection


@pytest.fixture(scope='module')
def tfi(request, tfile):
    """Return a taskfile info for the taskfile from the tfile fixture.

    This will also create a dummy file for the taskfileinfo.
    """
    tfi = TaskFileInfo(tfile.task, tfile.version, tfile.releasetype, tfile.typ, tfile.descriptor)
    jbf = JB_File(tfi)
    jbf.create_directory()
    with open(jbf.get_fullpath(), 'w') as f:
        f.write('Hello\n')

    def fin():
        os.remove(jbf.get_fullpath())
    request.addfinalizer(fin)
    return tfi


@pytest.fixture(scope='function')
def success_checks(successf):
    """Return an action collection with a successing check"""
    au = ActionUnit("SuccessUnit", "this unit should always succeed", successf)
    return ActionCollection([au])


@pytest.fixture(scope='function')
def success_cleanup(successf):
    """Return an action collection with a successing check"""
    au = ActionUnit("SuccessUnit", "this unit should always succeed", successf)
    return ActionCollection([au])


@pytest.fixture(scope='function')
def release_instance(tfi, success_checks, success_cleanup):
    """Return a Release that should have successing checks and successing cleanups.

    The comment for the release is \"A comment.\"
    """
    return release.Release(tfi, success_checks, success_cleanup, "A comment.")

