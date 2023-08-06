import argparse

from .commands import Command

DEFAULT_NUM_OF_REPOS = 10
BASE_GITHUB_API_ENDPOINT = 'https://api.github.com/'
MAP_CMD_TO_CLASS = {cmd.name(): cmd for cmd in vars()[Command.__name__].__subclasses__()}

def init_parser():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='ghtool', description='GitHub command line tool.')
    subparsers = parser.add_subparsers(help='List of commands', dest='cmd')

    # create the parser for the 'list' command
    parser_list = subparsers.add_parser('list', help='list help')
    parser_list.add_argument('language', help='programming language', nargs='?')
    parser_list.add_argument('-n', type=int, help='number of repositories to show (DEFAULT: {})'.format(DEFAULT_NUM_OF_REPOS), default=DEFAULT_NUM_OF_REPOS)

    # create the parser for the 'desc' command
    parser_desc = subparsers.add_parser('desc', help='desc help')
    parser_desc.add_argument('repo_ids', help='Language help', nargs='*')

    return parser
