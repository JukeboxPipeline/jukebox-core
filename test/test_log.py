import jukeboxcore.log as log


def test_get_logger():
    """Try to obtain a default logger"""
    l = log.get_logger(__name__)
    l.debug("Success")
