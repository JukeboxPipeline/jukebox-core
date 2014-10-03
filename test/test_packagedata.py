import os

from jukeboxcore.constants import MAIN_STYLESHEET, CORE_CONFIG_SPEC_PATH


def test_resources():
    assert os.path.exists(MAIN_STYLESHEET)
    assert os.path.exists(CORE_CONFIG_SPEC_PATH)
