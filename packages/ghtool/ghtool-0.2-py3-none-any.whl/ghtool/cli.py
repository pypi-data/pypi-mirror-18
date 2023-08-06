'''
This module contains method for console entry point
'''
from ghtool import init_parser, MAP_CMD_TO_CLASS
import sys

def main():
    '''
    This method parses input arguments and returns
    result (text) of specific command execution or
    displays help.
    '''
    parser = init_parser()
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args.cmd == 'desc' and not args.repo_ids:
            return parser.parse_args(['desc', '-h'])
        MAP_CMD_TO_CLASS[args.cmd](args).execute()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
