'''
This module contains method for initializing argument parser.
It also contains dynamically built dictionary with items
command_name: COMMAND_SUBCLASS.
'''
import argparse

from .commands import Command

command_subclasses = vars()[Command.__name__].__subclasses__()

MAP_CMD_TO_CLASS = {cmd.name(): cmd for cmd in command_subclasses}

def init_parser():
    '''
    This method returns parser for input arguments.
    '''
    parser = argparse.ArgumentParser(prog='ghtool', description='GitHub command line tool.')
    subparsers = parser.add_subparsers(help='List of commands', dest='cmd')
    for cmd in command_subclasses:
        cmd.add_cmd_subparser(subparsers)

    return parser
