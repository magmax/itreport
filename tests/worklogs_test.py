from unittest import TestCase

import yaml
from jiradump.writer import Worklog


class WorklogTest(TestCase):
    def load_issue(self, id):
        with open(f"tests/{id}.yaml") as fd:
            return yaml.load(fd, Loader=yaml.FullLoader)

    def test_no_work(self):
        issue = self.load_issue("IS-2")
        worklog = Worklog()
        worklog.add(issue)
        assert worklog.users == {}
        assert worklog.issues == {}

    def test_some_work(self):
        issue = self.load_issue("IS-1")
        worklog = Worklog()
        worklog.add(issue)
        assert worklog.users == {
            "fubar": [
                {
                    "issueId": "1001",
                    "issueKey": "IS-1",
                    "started": "2019-12-19T00:00:00.000+0100",
                    "timeSpent": "30m",
                    "timeSpentSeconds": 1800,
                    "userKey": "fubar",
                    "userName": "fubar",
                    "userDisplayName": "Fubar",
                    "comment": "A comment for the worklog",
                }
            ]
        }
        assert worklog.issues == {
            "IS-1": [
                {
                    "issueId": "1001",
                    "issueKey": "IS-1",
                    "started": "2019-12-19T00:00:00.000+0100",
                    "timeSpent": "30m",
                    "timeSpentSeconds": 1800,
                    "userKey": "fubar",
                    "userName": "fubar",
                    "userDisplayName": "Fubar",
                    "comment": "A comment for the worklog",
                }
            ]
        }
