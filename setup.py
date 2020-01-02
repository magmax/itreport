# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

from itreport import __version__


def read_description():
    try:
        with open("README.rst", encoding="utf8") as fd:
            return fd.read()
    except TypeError:
        with open("README.rst") as fd:
            return fd.read()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args or ["--cov-report=term-missing"])
        sys.exit(errno)


setup(
    name="itreport",
    version=__version__,
    description=("Data gatherer and final data report generator."),
    long_description=read_description(),
    cmdclass={"test": PyTest},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="jira atlassian it report",
    author="Miguel Ángel García",
    author_email="miguelangel.garcia@gmail.com",
    url="https://github.com/magmax/itreport",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["jira == 2.0.0", "pyyaml == 5.2", "jinja2 == 2.10.3"],
    entry_points={
        "console_scripts": [
            "itr-jiradump = itreport.jiradump:main",
            "itreport = itreport.report:main",
        ]
    },
)
