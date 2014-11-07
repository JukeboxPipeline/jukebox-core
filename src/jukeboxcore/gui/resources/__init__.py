"""Module with compiled resources that can be registered by importing them."""
import os
import pkgutil
import sys


def load_all_resources():
    """Load all resources inside this package

    When compiling qt resources, the compiled python file will register the resource
    on import.

    .. Warning:: This will simply import all modules inside this package
    """
    dirname = os.path.dirname(__file__)
    for importer, mod_name, _ in pkgutil.iter_modules([dirname]):
        full_mod_name = '%s.%s' % (dirname, mod_name)
        if full_mod_name not in sys.modules:
            module = importer.find_module(mod_name
                        ).load_module(full_mod_name)
            print "Loaded: %s" % module
