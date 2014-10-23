#!/usr/bin/env python
"""This is the launcher for all pipeline related launching operations

This launcher is used for console_scripts and gui_scripts entry points of setuptools.
It is used for all commandline actions of the pipeline.
For useage execute::

  jukebox -h

This requires jukeboxcore to be installed via setuptools (pip or easy_install will do that for you). You can also execute this script directly.

It's duty is to initialize the pipeline and then launch whatever plugin is requested.
It also mirrors the django manage commands of manage.py.
"""
import argparse
import sys

from jukeboxcore import main, plugins, gui
from jukeboxcore.gui import compile_ui


class Launcher(object):
    """Provides commands and handles argument parsing
    """

    def __init__(self, ):
        """Initialize parsers

        :raises: None
        """
        super(Launcher, self).__init__()
        self.parser = self.setup_core_parser()
        self.subparsers = self.setup_cmd_subparsers(self.parser)
        launchp = self.subparsers.add_parser("launch",
                                             help="Launches addons for jukebox.")
        listp = self.subparsers.add_parser("list",
                                           help="List all addons that can be launched with the launch command.")
        managep = self.subparsers.add_parser("manage", add_help=False,
                                             help="Manage django command")
        compileuip = self.subparsers.add_parser("compileui", help="Compile Qt Designer Files")
        self.setup_launch_parser(launchp)
        self.setup_list_parser(listp)
        self.setup_manage_parser(managep)
        self.setup_compile_ui_parser(compileuip)

    def setup_core_parser(self, ):
        """Setup the core parser

        :returns: the parser
        :rtype: :class:`argparse.ArgumentParser`
        :raises: None
        """
        parser = argparse.ArgumentParser()
        return parser

    def setup_cmd_subparsers(self, parser):
        """Add a subparser for commands to the given parser

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: the subparser action object
        :rtype: action object
        :raises: None
        """
        subparsers = parser.add_subparsers(title="commands",
                                           help="available commands")
        return subparsers

    def setup_launch_parser(self, parser):
        """Setup the given parser for the launch command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.launch)
        parser.add_argument("addon", help="The jukebox addon to launch. The addon should be a standalone plugin.")

    def launch(self, args, unknown):
        """Launch something according to the provided arguments

        :param args: arguments from the launch parser
        :type args: Namespace
        :param unknown: list of unknown arguments
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: SystemExit
        """
        pm = plugins.PluginManager.get()
        addon = pm.get_plugin(args.addon)
        isgui = isinstance(addon, plugins.JB_CoreStandaloneGuiPlugin)
        if isgui:
            gui.main.init_gui()
        print "Launching %s..." % args.addon
        addon.run()
        if isgui:
            app = gui.main.get_qapp()
            sys.exit(app.exec_())

    def setup_list_parser(self, parser):
        """Setup the given parser for the list command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.list)

    def list(self, args, unknown):
        """List all addons that can be launched

        :param args: arguments from the launch parser
        :type args: Namespace
        :param unknown: list of unknown arguments
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: None
        """
        pm = plugins.PluginManager.get()
        plugs = pm.get_all_plugins()
        if not plugs:
            print "No standalone addons found!"
            return
        print "Addons:"
        for p in plugs:
            if isinstance(p, plugins.JB_CoreStandalonePlugin):
                print "\t%s" % p.__class__.__name__

    def setup_manage_parser(self, parser):
        """Setup the given parser for manage command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.manage)
        parser.add_argument("args", nargs=argparse.REMAINDER,
                            help="arguments for django manage command")

    def manage(self, namespace, unknown):
        """Execute the manage command for django

        :param namespace: namespace containing args with django manage.py arguments
        :type namespace: Namespace
        :param unknown: list of unknown arguments that get passed to the manage.py command
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: None
        """
        # first argument is usually manage.py. This will also adapt the help messages
        args = ['jukebox manage']
        args.extend(namespace.args)
        args.extend(unknown)
        from django.core.management import execute_from_command_line
        execute_from_command_line(args)

    def setup_compile_ui_parser(self, parser):
        """Setup the given parser for the compile command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.compile_ui)
        parser.add_argument('uifile',
                        help='the uifile that will be compiled.\
The compiled file will be in the same directory but ends with _ui.py',
                        type=argparse.FileType('r'))

    def compile_ui(self, namespace, unknown):
        """Compile qt designer files

        :param args: arguments from the launch parser
        :type args: Namespace
        :param unknown: list of unknown arguments
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: None
        """
        uifile = namespace.uifile.name
        compile_ui.compile(uifile)

    def parse_args(self, args=None):
        """Parse the given arguments

        All commands should support executing a function,
        so you can use the arg Namespace like this::

          launcher = Launcher()
          args, unknown = launcher.parse_args()
          args.func(args, unknown) # execute the command

        :param args: arguments to pass
        :type args:
        :returns: the parsed arguments and all unknown arguments
        :rtype: (Namespace, list)
        :raises: None
        """
        if args is None:
            args = sys.argv[1:]
        return self.parser.parse_known_args(args)


def main_func(args=None):
    """Main funcion when executing this module as script

    :param args: commandline arguments
    :type args: list
    :returns: None
    :rtype: None
    :raises: None
    """
    main.init()
    launcher = Launcher()
    parsed, unknown = launcher.parse_args(args)
    parsed.func(parsed, unknown)

if __name__ == '__main__':
    main_func()
