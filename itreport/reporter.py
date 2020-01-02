import logging
import os

import jinja2

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self, output_dir):
        loader = jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader("./templates"),
                jinja2.FileSystemLoader(
                    os.path.join(os.path.expanduser("~"), ".itreport", "templates")
                ),
                jinja2.FileSystemLoader("/etc/itreport/templates"),
                jinja2.PackageLoader("itreport", "templates"),
            ]
        )
        self.env = jinja2.Environment(loader=loader)
        self.output = output_dir

    def apply(self, template_name, values):
        output_file = os.path.join(self.output, template_name)
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logger.info(f"Applying template {template_name} and saving as {output_file}")
        template = self.env.get_template(template_name)
        with open(output_file, "w+") as fd:
            fd.write(template.render(**values))
