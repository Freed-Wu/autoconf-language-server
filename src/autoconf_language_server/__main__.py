r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from contextlib import suppress
from datetime import datetime

from . import __version__

VERSION = rf"""autoconf_language_server {__version__}
Copyright (C) {datetime.now().year}
Written by Wu Zhenyu
"""
EPILOG = """
Report bugs to <wuzhenyu@ustc.edu>.
"""


def get_parser():
    r"""Get a parser for unit test."""
    parser = ArgumentParser(
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", version=VERSION, action="version")
    with suppress(ImportError):
        import shtab

        shtab.add_argument_to(parser)
    return parser


def main():
    r"""Parse arguments and provide shell completions."""
    parser = get_parser()
    parser.parse_args()

    from . import __name__
    from .server import AutoconfLanguageServer

    AutoconfLanguageServer(__name__.replace("_", "-"), __version__).start_io()


if __name__ == "__main__":
    main()
