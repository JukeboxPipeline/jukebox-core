"""The config module manages writing and loading of user preferences

We use `ConfigObj Module <https://pypi.python.org/pypi/configobj/>`_.
With its help, we can read and write **ini**-files.
We are also able to validate it against a specification ini, so there are
always correct values after loading.

Use the :mod:`jukeboxcore.iniconf` module for loading the core config file.
As a plugin developer, use :func:`jukeboxcore.plugins.JB_Plugin.get_config` to obtain the ConfigObj.
The ConfigObj behaves like a dictionary. It will have all keys, that you specified in your
spec file.

.. important:: Make sure that every value in your config specification has a valid default value!

For editing a configfile there is the Configer plugin.

"""
import os

from configobj import ConfigObj, flatten_errors
from validate import Validator

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore.errors import ConfigError
from jukeboxcore.constants import CORE_CONFIG_PATH, CORE_CONFIG_SPEC_PATH


def get_section_path(section):
    """Return a list with keys to access the section from root

    :param section: A Section
    :type section: Section
    :returns: list of strings in the order to access the given section from root
    :raises: None
    """
    keys = []
    p = section
    for i in range(section.depth):
        keys.insert(0, p.name)
        p = p.parent
    return keys


def check_default_values(section, key, validator=None):
    """Raise an MissingDefaultError if a value in section does not have a default values

    :param section: the section of a configspec
    :type section: section
    :param key: a key of the section
    :type key: str
    :param validator: a Validator object to get the default values
    :type validator: Validator
    :returns: None
    :raises: MissingDefaultError

    Use this in conjunction with the walk method of a ConfigObj.
    The ConfigObj should be the configspec!
    When you want to use a custom validator, try::

      configinstance.walk(check_default_values, validator=validatorinstance)

    """
    if validator is None:
        validator = Validator()
    try:
        validator.get_default_value(section[key])
    except KeyError:
        #dv = set(section.default_values.keys())  # set of all defined default values
        #scalars = set(section.scalars)  # set of all keys
        #if dv != scalars:
        parents = get_section_path(section)
        msg = 'The Key %s in the section %s is missing a default: %s' % (key, parents, section[key])
        log.debug(msg)
        raise ConfigError(msg)


def fix_errors(config, validation):
    """Replace errors with their default values

    :param config: a validated ConfigObj to fix
    :type config: ConfigObj
    :param validation: the resuts of the validation
    :type validation: ConfigObj
    :returns: The altered config (does alter it in place though)
    :raises: None
    """
    for e in flatten_errors(config, validation):
        sections, key, err = e
        sec = config
        for section in sections:
            sec = sec[section]
        if key is not None:
            sec[key] = sec.default_values.get(key, sec[key])
        else:
            sec.walk(set_to_default)
    return config


def set_to_default(section, key):
    """Set the value of the given seciton and key to default

    :param section: the section of a configspec
    :type section: section
    :param key: a key of the section
    :type key: str
    :returns: None
    :raises: None
    """
    section[key] = section.default_values.get(key, section[key])


def clean_config(config):
    """Check if all values have defaults and replace errors with their default value

    :param config: the configobj to clean
    :type config: ConfigObj
    :returns: None
    :raises: ConfigError

    The object is validated, so we need a spec file. All failed values will be replaced
    by their default values. If default values are not specified in the spec, a
    MissingDefaultError will be raised. If the replaced values still fail validation,
    a ValueError is raised. This can occur if the default is of the wrong type.

    If the object does not have a config spec, this function does nothing.
    You are on your own then.
    """
    if config.configspec is None:
        return
    vld = Validator()
    validation = config.validate(vld, copy=True)
    config.configspec.walk(check_default_values, validator=vld)
    fix_errors(config, validation)
    validation = config.validate(vld, copy=True)
    if not (validation == True):  # NOQA seems unpythonic but this validation evaluates that way only
        msg = 'The config could not be fixed. Make sure that all default values have the right type!'
        log.debug(msg)
        raise ConfigError(msg)


def load_config(f, spec):
    """Return the ConfigObj for the specified file

    :param f: the config file path
    :type f: str
    :param spec: the path to the configspec
    :type spec: str
    :returns: the loaded ConfigObj
    :rtype: ConfigObj
    :raises: ConfigError
    """
    dirname = os.path.dirname(f)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    c = ConfigObj(infile=f, configspec=spec,
                  interpolation=False, create_empty=True)
    try:
        clean_config(c)
    except ConfigError, e:
        msg = "Config %s could not be loaded. Reason: %s" % (c.filename, e)
        log.debug(msg)
        raise ConfigError(msg)
    return c


def get_core_config():
    """Return the ConfigObj of the main jukebox config file

    :returns: the loaded ConfigObj
    :rtype: ConfigObj
    :raises: None
    """
    f = CORE_CONFIG_PATH
    spec = CORE_CONFIG_SPEC_PATH
    return load_config(f, spec)
