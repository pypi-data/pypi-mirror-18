from ghtool import init_parser, MAP_CMD_TO_CLASS
import sys

def main():
    parser = init_parser()
    if len(sys.argv) > 1:
        args = parser.parse_args()
        MAP_CMD_TO_CLASS[args.cmd](args).execute()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
