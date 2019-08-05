"""Habrproxy command-line util."""

import logging
import sys
from argparse import ArgumentParser
from habrproxy.proxy import app, LOGGER_NAME

DEFAULT_REMOTE_ADDRESS = "https://habr.com"
DEFAULT_LOCAL_PORT = 8080


def configure_logger(enable_debug):
    """Configure module logger output."""
    level = logging.DEBUG if enable_debug else logging.INFO
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
    handler.setLevel(level)
    logger.addHandler(handler)


def main():
    """Habrproxy command-line util main routine."""
    parser = ArgumentParser(description="Habrproxy")
    parser.add_argument(
        "-r",
        "--remote-address",
        type=str,
        default=DEFAULT_REMOTE_ADDRESS,
        help="Remote address (e.g. http://k-vinogradov.ru)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_LOCAL_PORT,
        help="Local proxy port number",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug output"
    )
    args = parser.parse_args()
    configure_logger(args.verbose)
    app(args.remote_address, args.port)

if __name__ == "__main__":
    main()
