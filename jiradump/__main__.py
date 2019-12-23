#!/usr/bin/env python
import argparse
import datetime
import logging

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


def valid_date(s):
    valid_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]
    for fmt in valid_formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    msg = "Not a valid date: '{0}'. Valid formats: {1}".format(s, ",".join(valid_formats))
    raise argparse.ArgumentTypeError(msg)


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor for HTTP traffic")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("-s", "--server", help="Server to connect to")
    parser.add_argument(
        "-f",
        "--from-date",
        type=datetime.datetime,
        help="Date from to get data (format: YYYY/MM/DD)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(args.verbose)

    server = args.server or input("Server: ")
    jiradump = JiraDump(server)
    jiradump.dump(
        jiradump.retrieve(
            datetime.datetime(2019, 12, 13), datetime.datetime(2019, 12, 20)
        ),
        "output",
    )


if __name__ == "__main__":
    main()
