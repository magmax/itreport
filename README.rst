Quick SetUp
===========

Jiradump uses python-jira, so it can use the `.netrc` file too.

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

After this easy initialization, just download the repository and run::

    python -m jiradump -s example.atlassian.net

And it will dump the issues that were modified in the selected period or are
currently open. The default period is "today", but you can change it with the
options `-f` and `-t`.
