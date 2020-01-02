Quick SetUp
===========

ITReport uses python-jira, so it can use the `.netrc` file too.

The easiest setup is:

1. Get an api token. If you are using Jira Cloud, you can get it at
   https://id.atlassian.com/manage/api-tokens

2. Edit the `~/.netrc` file with an entry like::

       machine <uri to your jira instance>
         login <your username>
         password <the jira token>

   example::

       machine example.atlassian.net
         login fubar@example.org
         password ASDFHUdflasfj867ua

3. Install itreport::

    pip install itreport


This installs some scripts:

jiradump
--------

Dumps jira issues, authors and more into yaml files.

Example:

    itr-jiradump --server example.atlassian.net --project EX

itreport
--------

Applies some templates in order to generate a final report.

Example:

    itreport -t issue.rst -vvv

