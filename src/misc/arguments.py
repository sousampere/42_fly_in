
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
    """Parse arguments

    Returns:
        Namespace: arguments object
    """
    parser = ArgumentParser(
        prog='Fly-in to the moon !',
        description="A 42 project realised by gtourdia.",
        epilog="Made with ♥ by gtourdia :)"
    )

    parser.add_argument(
        '-i', '--input',
        help='Path of the input file',
        default='maps/easy/01_linear_path.txt',
        required=False
    )

    return parser.parse_args()
