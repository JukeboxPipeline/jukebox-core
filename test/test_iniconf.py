from configobj import ConfigObj
from validate import Validator
from nose.tools import eq_

import jukeboxcore.iniconf as iniconf
from jukeboxcore.errors import ConfigError

spec = ConfigObj(interpolation=False, list_values=False,
                 _inspec=True)
spec['key1'] = 'integer(max=20, default=10)'
spec['key2'] = 'string_list(max=3, min=3, default=list(\"c\", \"d\", \"e\"))'
spec['key3'] = 'integer'

c = ConfigObj(configspec=spec)
c['sec1'] = {'sec2': {'sec3': {}}}
c['key1'] = 'abc'
c['key2'] = ('a', 'b', 'c')


def test_get_core_config():
    """Try to get the core config"""
    iniconf.get_core_config()


def test_get_section_path():
    """Get the section path to a section"""
    sp = iniconf.get_section_path(c['sec1'])
    errmsg = "Section path is not as expected!"
    assert sp == ['sec1'], errmsg
    sp = iniconf.get_section_path(c['sec1']['sec2'])
    assert sp == ['sec1', 'sec2'], errmsg
    sp = iniconf.get_section_path(c['sec1']['sec2']['sec3'])
    assert sp == ['sec1', 'sec2', 'sec3'], errmsg


def test_check_default_values():
    """check default values in conf"""
    iniconf.check_default_values(spec, 'key1')
    iniconf.check_default_values(spec, 'key2')
    try:
        iniconf.check_default_values(spec, 'key3')
    except ConfigError:
        spec['key3'] = 'integer(default=1)'
    else:
        raise AssertionError("Checking for a default value should have failed with: %s" % spec['key3'])


def test_fix_errors():
    """Fix Errors of config"""
    vld = Validator()
    result = c.validate(vld)
    iniconf.fix_errors(c, result)
    assert c['key1'] == 10, """The config should have been fixed. But key1 is %s instead of 10""" % c['key1']


def test_set_to_default():
    """Set key in config to default"""
    eq_(c['key2'], ['a', 'b', 'c'])
    iniconf.set_to_default(c, 'key2')
    assert c['key2'] == ['c', 'd', 'e'], """The config should have key2 set to its default. But its %s""" % c['key2']


def test_clean_config():
    """clean a config"""
    iniconf.clean_config(c)
