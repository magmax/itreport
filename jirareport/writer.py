import logging
import os

import yaml

logger = logging.getLogger(__name__)


class Writer:
    def __init__(self, output):
        self.output = output

    def write(self, issues, extractor, namer):
        if not os.path.exists(self.output):
            logger.debug(f"Creating directory {self.output}")
            os.makedirs(self.output)

        for issue in issues:
            with open(os.path.join(self.output, namer(issue)), "w+") as fd:
                yaml.dump(extractor(issue), fd, default_flow_style=False)
