import pytest

from jukeboxcore.action import ActionCollection, ActionUnit, ActionStatus


@pytest.fixture(scope='session')
def successstatus():
    return  ActionStatus(ActionStatus.SUCCESS, "Success", "")


@pytest.fixture(scope='session')
def failstatus():
    return  ActionStatus(ActionStatus.FAILURE, "Failure", "")


@pytest.fixture(scope='session')
def errorstatus():
    return  ActionStatus(ActionStatus.ERROR, "Error", "some traceback")


@pytest.fixture(scope='session')
def skippedstatus():
    return ActionStatus(ActionStatus.SKIPPED, "Skipped", "")


@pytest.fixture(scope='function')
def succeededunit1(successstatus, successf):
    succeededunit1 = ActionUnit("SucceedingUnit1", "", successf)
    succeededunit1.status = successstatus
    return succeededunit1


@pytest.fixture(scope='function')
def succeededunit2(successstatus, successf):
    succeededunit2 = ActionUnit("SucceedingUnit2", "", successf)
    succeededunit2.status = successstatus
    return succeededunit2


@pytest.fixture(scope='function')
def erroredunit(errorstatus, errorf):
    erroredunit = ActionUnit("ErrorUnit", "", errorf)
    erroredunit.status= errorstatus
    return erroredunit


@pytest.fixture(scope='function')
def failedunit(failstatus, failf):
    failedunit = ActionUnit("FailUnit", "", failf)
    failedunit.status = failstatus
    return failedunit


@pytest.fixture(scope='function')
def skippedunit(skippedstatus, successf):
    skippedunit = ActionUnit("SkipUnit", "", successf)
    skippedunit.status = skippedstatus
    return skippedunit


@pytest.fixture(scope='function')
def nonefunction():
    """Return a function that returns None"""
    def f():
        return None
    return f


def test_status():
    s = ActionStatus()
    assert s.value is None
    assert s.message == "Not executed."
    assert s.traceback == ""

    s = ActionStatus(ActionStatus.SUCCESS)
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Not executed."
    assert s.traceback == ""

    msg = "Nothing"
    traceback = "Some traceback"
    s = ActionStatus(msg=msg, traceback=traceback)
    assert s.value is None
    assert s.message == msg
    assert s.traceback == traceback


def test_action_error(errorf):
    """Test if action that raises an error catches the error and saves traceback"""
    au = ActionUnit("ErrorFunc", "Raises an exception", errorf)
    au.run(None)

    s = au.status
    assert s.value is ActionStatus.ERROR
    assert s.message == "Unexpected Error."
    assert s.traceback


def test_action_return_status(nonefunction, successf):
    """Test if when action returns no status, an error status is created instead"""
    niceu = ActionUnit("NiceUnit", "Returns status", successf)
    badu = ActionUnit("BadUnit", "Does not return status", nonefunction)

    niceu.run(None)
    s = niceu.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback

    badu.run(None)
    s = badu.status
    assert s.value is ActionStatus.ERROR
    assert s.message == "Unexpected Error."
    assert s.traceback


def test_action_depsuccess(succeededunit1, skippedunit, succeededunit2, erroredunit, failedunit, successf):
    """Test if action gets skipped if other actions are unsuccessful"""
    d = [succeededunit2, failedunit, erroredunit, succeededunit2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"FailUnit\" did not succeed."
    assert not s.traceback

    d = [succeededunit1, erroredunit, failedunit, succeededunit2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"ErrorUnit\" did not succeed."
    assert not s.traceback

    d = [succeededunit1, skippedunit, erroredunit, succeededunit2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SkipUnit\" did not succeed."
    assert not s.traceback

    d = [succeededunit1, succeededunit2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback


def test_action_depfail(skippedunit, succeededunit1, succeededunit2, erroredunit, failedunit, successf):
    """Test if action gets skipped if other actions are successful"""
    d = [erroredunit, failedunit, succeededunit1, succeededunit2]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SucceedingUnit1\" did not fail."
    assert not s.traceback

    d = [erroredunit, failedunit, succeededunit2, succeededunit1]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SucceedingUnit2\" did not fail."
    assert not s.traceback

    d = [erroredunit]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback

    d = [failedunit]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback

    d = [skippedunit]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback


def test_actioncollection_status(skippedunit, succeededunit1, succeededunit2, erroredunit, failedunit):
    """Test if actioncollection status is calculated right."""
    ac = ActionCollection([succeededunit1, skippedunit, succeededunit2])
    s = ac.status()
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "All actions succeeded."
    assert s.traceback == ""

    ac = ActionCollection([succeededunit1, failedunit, failedunit, erroredunit, failedunit, skippedunit, succeededunit2])
    s = ac.status()
    assert s.value is ActionStatus.ERROR
    assert s.message == "Error: action \"ErrorUnit\" raised an error!"
    assert s.traceback

    ac = ActionCollection([succeededunit1, failedunit, failedunit, skippedunit, succeededunit2])
    s = ac.status()
    assert s.value is ActionStatus.FAILURE
    assert s.message == "Action(s) failed!"
    assert s.traceback == ""


def test_actioncollection_execute(successstatus):
    """Test if all actions are run correctly"""
    def append1(l):
        l.append(1)
        return successstatus

    def append2(l):
        l.append(2)
        return successstatus

    au1 = ActionUnit("append1", "append 1 to list", append1)
    au2 = ActionUnit("append2", "append 2 to list", append2)
    au3 = ActionUnit("append1", "append 1 to list", append1)
    ac = ActionCollection([au1, au2, au3])
    l = [3, 4, 5]
    ac.execute(l)
    s = ac.status()
    assert s.value is ActionStatus.SUCCESS
    assert l == [3, 4, 5, 1, 2, 1]
