import os

#from pkg_resources import resource_filename

from jukeboxcore.constants import MAIN_STYLESHEET


def test_resources():
    assert os.path.exists(MAIN_STYLESHEET)
