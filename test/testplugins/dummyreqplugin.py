from jukeboxcore.plugins import JB_CorePlugin


class DummyReqPlugin(JB_CorePlugin):
    """ Test the require functionality of plugins """

    required = ("DummyPlugin",)

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
