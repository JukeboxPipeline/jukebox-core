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
def fail_checks(failf):
    """Return an action collection with failing check"""
    au = ActionUnit("FailUnit", "this unit should always fail", failf)
    return ActionCollection([au])


@pytest.fixture(scope='function')
def success_cleanup(successf):
    """Return an action collection with a successing cleanup"""
    au = ActionUnit("SuccessUnit", "this unit should always succeed", successf)
    return ActionCollection([au])


@pytest.fixture(scope='function')
def fail_cleanup(failf):
    """Return an action collection with failing cleanup"""
    au = ActionUnit("FailUnit", "this unit should always fail", failf)
    return ActionCollection([au])


@pytest.fixture(scope='function',
                params=[("success_checks", "success_cleanup"),
                        ("fail_checks", "fail_cleanup")])
def release_instance(request, tfi):
    """Return a Release that should have successing checks and successing cleanups.

    The comment for the release is \"A comment.\"
    """
    check = request.getfuncargvalue(request.param[0])
    cleanup = request.getfuncargvalue(request.param[1])
    r = release.Release(tfi, check, cleanup, "A comment.")

    def returnTrue(*args, **kwargs):
        return True
    r.confirm_check_result = returnTrue
    return r


def test_release(release_instance):
    release_instance.release()
