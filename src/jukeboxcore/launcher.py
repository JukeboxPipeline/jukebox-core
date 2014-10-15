#!/usr/bin/env python
"""This is the launcher for all pipeline related launching operations

This launcher is used for console_scripts and gui_scripts entry points of setuptools.
It is used for all commandline actions of the pipeline.
It's duty is to initialize the pipeline and then launch whatever plugin is requested.
"""
import argparse
import sys


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
        launchp = self.subparsers.add_parser("launch", help="Launches addons for jukebox.")
        self.setup_launch_parser(launchp)

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

        :param parser:
        :type parser:
        :returns: the subparser action object
        :rtype: action object
        :raises: None
        """
        subparsers = parser.add_subparsers(title="commands",
                                           help="available commands")
        return subparsers

    def setup_launch_parser(self, parser):
        """Setup the given parser for the launch command

        :param parser:
        :type parser:
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.launch)
        parser.add_argument("addon", help="The jukebox addon to launch. The addon should be a standalone plugin.")

    def launch(self, args):
        """Launch something according to the provided arguments

        :param args: arguments from the launch parser
        :type args: Namespace
        :returns: None
        :rtype: None
        :raises: None
        """
        print "launching with %s" % args

if __name__ == '__main__':
    launcher = Launcher()
    args = launcher.parser.parse_args(sys.argv[1:])
    args.func(args)
