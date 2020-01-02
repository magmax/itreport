import logging
import os

import yaml

logger = logging.getLogger(__name__)


class Writer:
    def __init__(self, output):
        self.output = output

    def write(self, resources, extractor, namer):
        for res in resources:
            with open(os.path.join(self.output, namer(res)), "w+") as fd:
                yaml.dump(extractor(res), fd, default_flow_style=False)
