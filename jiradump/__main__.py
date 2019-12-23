#!/usr/bin/env python
import argparse
import configparser
import logging
import datetime
from getpass import getpass
import os

from .dump import JiraDump


logger = logging.getLogger(__name__)


def configure_logging(verbosity):
    msg_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    VERBOSITIES = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = VERBOSITIES[min(int(verbosity), len(VERBOSITIES) - 1)]
    formatter = logging.Formatter(msg_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor for HTTP traffic")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument(
        "-c", "--config-file", default='~/.jira/config.ini', help='Server to connect to'
    )
    parser.add_argument(
        "-s", "--server", help='Server to connect to'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(args.verbose)

    config = configparser.ConfigParser()
    config.read(os.path.expanduser(args.config_file))
    server = args.server or config['DEFAULT'].get('server') or input('Server: ')
    jiradump = JiraDump(server)
    jiradump.dump(
        jiradump.retrieve(
            datetime.datetime(2019, 12, 13),
            datetime.datetime(2019, 12, 20),
        ),
        'output'
    )


if __name__ == "__main__":
    main()#!/usr/bin/env python
