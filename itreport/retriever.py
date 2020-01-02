import logging

from jira import JIRA

logger = logging.getLogger(__name__)


class IssueIterator:
    def __init__(self, get_more, get_detail=None):
        self.data = None
        self.get_more = get_more
        self.get_detail = get_detail
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.data is None:
            self.data = self.get_more(0)
        if self.data.current + self.counter >= self.data.total:
            raise StopIteration()
        if self.counter == self.data.maxResults:
            self.data = self.get_more(self.data.current + self.data.maxResults)
            self.counter = 0

        result = self.data[self.counter]
        logger.info(
            f"Processing issue {self.data.current + self.counter + 1}/{self.data.total}:"
            f" {result.key}"
        )
        if self.get_detail:
            result = self.get_detail(result.key)
        self.counter += 1
        return result


class JiraRetriever:
    def __init__(self, server):
        self.jira = JIRA(server=server)
        self._users = set()

    def retrieve_issues(self, date_from, date_to, projects=None):
        str_from = date_from.strftime("%Y-%m-%d")
        str_to = date_to.strftime("%Y-%m-%d")

        def _internal(start_at):
            logger.info(f"Retrieving more issues starting at {start_at}")
            jql = f"(status != Closed OR (updated >= {str_from} AND updated <= {str_to}))"
            if projects:
                str_prj = ",".join(projects or [])
                jql += f" AND project in ({str_prj})"

            result = self.jira.search_issues(jql, startAt=start_at)
            self._extract_users_from_issues(result)
            return result

        return IssueIterator(_internal, self.jira.issue)

    def _extract_users_from_issues(self, issues):
        for issue in issues:
            fields = issue.raw["fields"]
            self._users.add((fields.get("assignee") or {}).get("key", None))
            self._users.add((fields.get("creator") or {}).get("key", None))

    def users(self):
        for user in self._users:
            if user is None:
                continue
            logger.info(f"Processing user {user}")
            yield self.jira.user(user, expand=["groups", "applicationRoles"])

    def fields(self):
        for f in self.jira.fields():
            logger.info(f"Processing custom field {f.get('key')}")
            yield f
