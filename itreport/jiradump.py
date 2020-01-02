#!/usr/bin/env python
import argparse
import datetime
import logging
import os

from .retriever import JiraRetriever
from .writer import Writer

logger = logging.getLogger(__name__)


def configure_logging(verbosity):
    msg_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    VERBOSITIES = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = VERBOSITIES[min(int(verbosity), len(VERBOSITIES) - 1)]
    formatter = logging.Formatter(msg_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger("itreport")
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def valid_date(s):
    valid_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]
    for fmt in valid_formats:
        try:
            return datetime.datetime.strptime(s, fmt)
        except ValueError:
            logger.debug(f"Date {s} does not match format {fmt}")
            pass
    msg = "Not a valid date: '{0}'. Valid formats: {1}".format(s, ",".join(valid_formats))
    raise argparse.ArgumentTypeError(msg)


def parse_args():
    parser = argparse.ArgumentParser(description="Dump Jira resources into YAML files")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    parser.add_argument("-s", "--server", help="Server to connect to")
    parser.add_argument(
        "-p", "--project", nargs="*", help="projects to be retrieved. All if empty"
    )
    parser.add_argument(
        "-f",
        "--from-date",
        type=valid_date,
        default=datetime.datetime.today(),
        help="Initial date to get data",
    )
    parser.add_argument(
        "-t",
        "--to-date",
        type=valid_date,
        default=datetime.datetime.today(),
        help="Final date to get data",
    )
    parser.add_argument("-o", "--output", default="build/dump", help="Output directory")
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(args.verbose)
    logger.info("Showing INFO messages")
    logger.debug("Showing DEBUG messages")

    if not os.path.exists(args.output):
        logger.debug(f"Creating directory {args.output}")
        os.makedirs(args.output)

    server = args.server or input("Server: ")
    logger.debug(f"Connecting to {server}")
    writer = Writer(args.output)
    retriever = JiraRetriever(server)
    issues = retriever.retrieve_issues(args.from_date, args.to_date, args.project)
    writer.write(issues, lambda x: x.raw, lambda x: f"issue-{x.key}.yaml")
    writer.write(retriever.users(), lambda x: x.raw, lambda x: f"user-{x.key}.yaml")
    writer.write(retriever.fields(), lambda x: x, lambda x: f"field-{x.get('key')}.yaml")


if __name__ == "__main__":
    main()
