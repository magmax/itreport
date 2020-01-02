#!/usr/bin/env python
import argparse
import logging
import os

from jirareport.reader import IssueWalker, UserWalker
from jirareport.reporter import Reporter

logger = logging.getLogger(__name__)


def configure_logging(verbosity):
    msg_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    VERBOSITIES = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = VERBOSITIES[min(int(verbosity), len(VERBOSITIES) - 1)]
    formatter = logging.Formatter(msg_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger("jirareport")
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def parse_args():
    parser = argparse.ArgumentParser(description="Translate jira resources to reports")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("-i", "--dump", default="build/dump", help="Input directory")
    parser.add_argument("-o", "--output", default="build/report", help="Output directory")
    parser.add_argument(
        "-t", "--template", nargs="*", help="Templates to be appled, comma separated"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(args.verbose)
    logger.info("Showing INFO messages")
    logger.debug("Showing DEBUG messages")

    if not os.path.exists(args.output):
        logger.debug(f"Creating directory {args.output}")
        os.makedirs(args.output)

    reporter = Reporter(args.output)
    values = dict(issues=IssueWalker(args.dump), users=UserWalker(args.dump))
    for template in args.template:
        reporter.apply(template, values)


if __name__ == "__main__":
    main()
