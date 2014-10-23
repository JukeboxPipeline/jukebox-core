from nose.tools import eq_
from configobj import ConfigObj
from PySide import QtCore

from jukeboxcore.gui.configeditor import ConfigObjModel


def get_sample_spec():
    """Return a configspec for testing

    :returns: :class:`ConfigObj`
    """
    spec = ConfigObj(interpolation=False, list_values=False,
                     _inspec=True)
    spec['k1'] = 'integer'
    spec['k2'] = 'integer(default=2)'
    spec['k3'] = 'integer(min=10, max=30)'
    spec['k4'] = 'string(default=\"test\")'
    spec['sec1'] = {'s1k1': 'string_list', 's1k2': 'string_list(default=list(\"a\", \"b\"))'}
    spec['sec1']['sec2'] = {'s2k1': 'string_list'}
    spec['sec1']['sec2']['sec3'] = {'s3k1': 'integer'}
    return spec


def get_sample_config():
    """Return a ConfigObj for testing

    :returns: :class:`ConfigObj`
    """
    conf = ConfigObj()
    conf['k1'] = 20
    conf['k3'] = 1
    conf['sec1'] = {'s1k1': ('\"a, b\", c', 'd')}
    return conf


class Test_ConfigObjModel():

    def test_model_wo_spec(self):
        """Test configobjmodel without spec"""
        model = ConfigObjModel(get_sample_config())
        voidi = QtCore.QModelIndex()
        sec1i = model.index(2, 0, voidi)
        #rowCount
        eq_(model.rowCount(voidi), 3)
        eq_(model.rowCount(model.index(2, 0, voidi)), 1)
        #data
        eq_(model.data(model.index(0, 0, voidi)), 'k1')
        eq_(model.data(model.index(1, 0, voidi)), 'k3')
        eq_(model.data(model.index(2, 0, voidi)), 'sec1')
        eq_(model.data(model.index(0, 1, voidi)), '20')
        eq_(model.data(model.index(1, 1, voidi)), '1')
        s1k1i = model.index(0, 1, sec1i)
        eq_(model.data(s1k1i), '(\'"a, b", c\', \'d\')')
        eq_(model.data(model.index(0, 2, voidi)), None)

    def test_model_wi_spec(self):
        """Test configobjmodel with spec"""
        spec = get_sample_spec()
        conf = get_sample_config()
        conf.configspec = spec
        model = ConfigObjModel(conf)
        voidi = QtCore.QModelIndex()
        sec1i = model.index(4, 0, voidi)
        #rowCount
        eq_(model.rowCount(voidi), 5)
        #data
        eq_(model.data(model.index(1, 1, voidi), QtCore.Qt.ForegroundRole).color(), model._invalid_col)

        #check correct stringlist rekursion
        eq_(model.data(sec1i), 'sec1')
        i = model.index(0, 0, sec1i)
        origdata = model.data(i)
        for j in range(5):
            model.setData(i, model.data(i))
            eq_(model.data(i), origdata)

    def test_val_to_str(self):
        """Test value to str conversion"""
        conf = get_sample_config()
        model = ConfigObjModel(conf)
        origvalues = ['1', 'hello', ['a', 'b', '"C", d'], ['1', '2', '3', '4'],
                      ['a', '\\ \\\\\"b\\\\"', 'c', 'd, f, "a, b,\\\\ \\ \\\ \\\\\\\ \\\'c,d\\\\\'"', 'g']]
        for origvalue in origvalues:
            value = origvalue
            for i in range(20):
                value = model._val_to_str(value)
                # _handle_value will parse it correctly
                (value, comment) = conf._handle_value(value)
                eq_(origvalue, value)
