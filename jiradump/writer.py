import logging
import os

import yaml

logger = logging.getLogger("jiradump." + __name__)


class Worklog:
    def __init__(self):
        self.users = {}
        self.issues = {}

    def as_dict(self):
        return dict(users=self.users, issues=self.issues)

    def add(self, issue):
        for w in issue.get("fields", {}).get("worklog", {}).get("worklogs", []):
            data = dict(
                issueId=w["issueId"],
                issueKey=issue["key"],
                started=w["started"],
                timeSpent=w["timeSpent"],
                timeSpentSeconds=w["timeSpentSeconds"],
                userKey=w["author"]["key"],
                userName=w["author"]["name"],
                userDisplayName=w["author"]["displayName"],
                comment=w.get("comment"),
            )
            if w["author"]["key"] not in self.users:
                self.users[w["author"]["key"]] = []
            self.users[w["author"]["key"]].append(data)

            if issue["key"] not in self.issues:
                self.issues[issue["key"]] = []
            self.issues[issue["key"]].append(data)


class Writer:
    def __init__(self, output):
        self.output = output

    def write(self, issues):
        if not os.path.exists(self.output):
            logger.debug(f"Creating directory {self.output}")
            os.makedirs(self.output)

        worklog = Worklog()

        for issue in issues:
            worklog.add(issue.raw)
            with open(os.path.join(self.output, f"{issue.key}.yaml"), "w+") as fd:
                yaml.dump(issue.raw, fd, default_flow_style=False)

        with open(os.path.join(self.output, "worklog.yaml"), "w+") as fd:
            yaml.dump(worklog.as_dict(), fd, default_flow_style=False)
