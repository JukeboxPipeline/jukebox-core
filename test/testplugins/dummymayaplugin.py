from jukebox.core.plugins import JB_MayaPlugin


class DummyMayaPlugin(JB_MayaPlugin):
    """ Tests the subclassing of JB_Plugin and has no functionality """

    def init(self, ):
        """ Reimplemented from JB_Plugin

        :returns:
        :rtype:
        :raises:
        """
        pass

    def uninit(self, ):
        """ Reimplemented from JB_Plugin

        :returns:
        :rtype:
        :raises:
        """
        pass
