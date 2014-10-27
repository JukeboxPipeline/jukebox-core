from jukeboxcore.fileaction import FileAction, ActionUnit, ActionStatus


def successf(f):
    return ActionStatus(ActionStatus.SUCCESS, "Success")


def errfunc(f):
    raise Exception


def failf(f):
    return ActionStatus(ActionStatus.FAILURE, "Failed")

sucstat = ActionStatus(ActionStatus.SUCCESS, "Success", "")
fstat = ActionStatus(ActionStatus.FAILURE, "Failure", "")
estat = ActionStatus(ActionStatus.ERROR, "Error", "some traceback")
skstat = ActionStatus(ActionStatus.SKIPPED, "Skipped", "")
dsuc1 = ActionUnit("SucceedingUnit1", "", None)
dsuc1.status = sucstat
dsuc2 = ActionUnit("SucceedingUnit2", "", None)
dsuc2.status = sucstat
derr = ActionUnit("ErrorUnit", "", None)
derr.status= estat
dfail = ActionUnit("FailUnit", "", None)
dfail.status = fstat
dsk = ActionUnit("SkipUnit", "", None)
dsk.status = skstat


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


def test_action_error():
    """Test if action that raises an error catches the error and saves traceback"""
    au = ActionUnit("ErrorFunc", "Raises an exception", errfunc)
    au.run(None)

    s = au.status
    assert s.value is ActionStatus.ERROR
    assert s.message == "Unexpected Error."
    assert s.traceback


def test_action_depsuccess():
    """Test if action gets skipped if other actions are unsuccessful"""
    d = [dsuc1, dfail, derr, dsuc2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"FailUnit\" did not succeed."
    assert not s.traceback

    d = [dsuc1, derr, dfail, dsuc2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"ErrorUnit\" did not succeed."
    assert not s.traceback

    d = [dsuc1, dsk, derr, dsuc2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SkipUnit\" did not succeed."
    assert not s.traceback

    d = [dsuc1, dsuc2]
    testau = ActionUnit("TestUnit", "", successf, d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback


def test_action_depfail():
    """Test if action gets skipped if other actions are successful"""
    d = [derr, dfail, dsuc1, dsuc2]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SucceedingUnit1\" did not fail."
    assert not s.traceback

    d = [derr, dfail, dsuc2, dsuc1]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SKIPPED
    assert s.message == "Skipped because action \"SucceedingUnit2\" did not fail."
    assert not s.traceback

    d = [derr]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback

    d = [dfail]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback

    d = [dsk]
    testau = ActionUnit("TestUnit", "", successf, depfail=d)
    testau.run(None)
    s = testau.status
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "Success"
    assert not s.traceback


def test_fileaction_status():
    """Test if fileaction status is calculated right."""
    fa = FileAction([dsuc1, dsk, dsuc2])
    s = fa.status()
    assert s.value is ActionStatus.SUCCESS
    assert s.message == "All actions succeeded."
    assert s.traceback == ""

    fa = FileAction([dsuc1, dfail, dfail, derr, dfail, dsk, dsuc2])
    s = fa.status()
    assert s.value is ActionStatus.ERROR
    assert s.message == "Error: action \"ErrorUnit\" raised an error!"
    assert s.traceback

    fa = FileAction([dsuc1, dfail, dfail, dsk, dsuc2])
    s = fa.status()
    assert s.value is ActionStatus.FAILURE
    assert s.message == "Action(s) failed!"
    assert s.traceback == ""