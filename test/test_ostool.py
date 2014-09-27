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
