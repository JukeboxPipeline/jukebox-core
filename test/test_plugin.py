import os

from jukeboxcore.plugins import PluginManager


def test_plugin_manager():
    """ Test Plugin Manager """
    os.environ['JUKEBOX_PLUGIN_PATH'] = os.path.abspath('jukebox/tests/testplugins')
    pmanager = PluginManager.get()
    pmanager.load_plugins()
    pmanager.unload_plugins()
    plugs = pmanager.get_all_plugins()
    dummy = pmanager.get_plugin('DummyPlugin')
    dummyreq = pmanager.get_plugin('DummyReqPlugin')
    assert plugs[-1] is dummyreq, "Last plugin to be loaded should be dummyreq plugin."
    assert plugs[-2] is dummy, "Dummy plugin should be required for dummyreq plugin, so it should be at second last position."

    assert pmanager is PluginManager.get()
