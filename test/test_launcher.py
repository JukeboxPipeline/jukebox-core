import pytest

from jukeboxcore.launcher import Launcher


@pytest.fixture()
def launcher():
    """Setup the launcher and return it

    :returns: the created launcher
    :rtype: :class:`jukeboxcore.launcher.Launcher`
    :raises: None
    """
    l = Launcher()
    return l


@pytest.mark.parametrize("argsinput",[["-h"],
                                      ["launch", "-h"],
                                      ["launch", "addon", "-h"],
                                      pytest.mark.xfail(["fail", "-h"])])
def test_launcher_help(argsinput, launcher):
    try:
        launcher.parse_args(argsinput)
    except SystemExit as e:
        if e.code != 0:
            raise e
