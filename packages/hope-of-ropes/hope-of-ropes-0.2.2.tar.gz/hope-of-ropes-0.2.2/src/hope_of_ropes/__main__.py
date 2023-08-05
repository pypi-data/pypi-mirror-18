import argparse
import hope_of_ropes
from hope_of_ropes import __version__


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Hope of Ropes')
    version = '%(prog)s ' + __version__
    parser.add_argument('--version', '-v', action='version', version=version)
    return parser

def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """
    print('oi')
    parser = get_parser()
    args = parser.parse_args(args)

    # Put your main script logic here
    print('No action defined for hope_of_ropes module!')


if __name__ == '__main__':
    main()