import sys
import argparse
from .toggle import toggle
from .settings import settings

def main():
    # arguments
    parser = argparse.ArgumentParser(description='')
    subparsers = parser.add_subparsers(help='')

    # start vpn toggle
    add_parser = subparsers.add_parser('start', help='start vpn toggle tray widget')
    add_parser.set_defaults(cmd=toggle.start)

    # configure vpn toggle
    add_parser = subparsers.add_parser('configure', help='configure vpn toggle tray widget')
    add_parser.set_defaults(cmd=settings.configure)

    # parse args and execute command
    args = parser.parse_args()
    if hasattr(args, 'cmd'):
        args.cmd()
        sys.exit()
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
