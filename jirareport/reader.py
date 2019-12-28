import logging
import os

import yaml

logger = logging.getLogger(__name__)


class IssuePromise:
    def __init__(self, path):
        self.filename = path
        self.data = None

    def __getattr__(self, attr):
        if self.data is None:
            logger.debug(f"loading details for {self.filename}")
            with open(self.filename) as fd:
                self.data = yaml.load(fd)
        return self.data.get(attr)


class IssueIterator:
    def __init__(self, files):
        self.files = list(files)

    def __next__(self):
        if not self.files:
            raise StopIteration()
        return IssuePromise(self.files.pop(0))


class IssueWalker:
    def __init__(self, directory):
        self.directory = directory

    def __iter__(self):
        return IssueIterator(
            os.path.join(self.directory, x)
            for x in os.listdir(self.directory)
            if x.startswith("issue-")
        )
