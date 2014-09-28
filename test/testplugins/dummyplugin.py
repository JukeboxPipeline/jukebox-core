from nose.tools import eq_

from jukeboxcore.plugins import JB_CorePlugin


class DummyPlugin(JB_CorePlugin):
    """ Tests the subclassing of JB_Plugin and has no functionality """

    def init(self, ):
        """ Reimplemented from JB_Plugin

        :returns:
        :rtype:
        :raises:
        """
        conf = self.get_config()
        eq_(conf['key1'], '20')
        eq_(conf['sec1']['key2'], 2)
        eq_(conf['sec1']['sec2']['key3'], ['a', 'b'])

    def uninit(self, ):
        """ Reimplemented from JB_Plugin

        :returns:
        :rtype:
        :raises:
        """
        pass
