#!/usr/bin/env python
"""This is the launcher for all pipeline related launching operations

This launcher is used for console_scripts and gui_scripts entry points of setuptools.
It is used for all commandline actions of the pipeline.
It's duty is to initialize the pipeline and then launch whatever plugin is requested.
"""
import argparse
import os
import sys

from jukeboxcore import main


class Launcher(object):
    """Launcher provides commands and handles argument parsing
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
        managep = self.subparsers.add_parser("manage", add_help=False,
                                             help="Manage django command")
        self.setup_launch_parser(launchp)
        self.setup_manage_parser(managep)

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
        :raises: None
        """
        print "launching with %s" % args

    def setup_manage_parser(self, parser):
        """Setup the given parser for manage command to

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
        # first argument is usually manage.py so we do this
        args = ['jukebox manage']
        args.extend(unknown)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jukeboxcore.djsettings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(args)

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
