from jukeboxcore import ostool


def test_detect_sys():
    """ Detect Platform

    :returns: None
    :rtype: None
    :raises: None
    """
    ostool.detect_sys()


def test_get_interface():
    """ Get PlatformInterface for your Platform

    :returns: None
    :rtype: None
    :raises: None
    """
    ostool.get_interface()


def test_interface():
    """ Run PlatformInterface methods

    :returns: None
    :rtype: None
    :raises: None
    """
    inter = ostool.get_interface()
    loc = inter.get_maya_location()
    assert loc
    site = inter.get_maya_sitepackage_dir()
    assert site
    mayapy = inter.get_maya_python()
    assert mayapy
    exe = inter.get_maya_exe()
    assert exe
