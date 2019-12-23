import yaml
import os
from jira import JIRA
from pprint import pprint
import logging


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
        if self.get_detail:
            result = self.get_detail(result.key)
        logger.debug(
            f'{self.data.current + self.counter+1}/'
            f'{self.data.total}/{self.counter}:'
            f'{result.key}'
        )
        self.counter += 1
        return result


class JiraDump:
    def __init__(self, server):
        self.jira = JIRA(server=server)

    def retrieve(self, date_from, date_to):
        str_from = date_from.strftime('%Y-%m-%d')
        str_to = date_to.strftime('%Y-%m-%d')

        def _internal(start_at):
            return self.jira.search_issues(
                'project = DVOP AND ('
                '  status != Closed OR'
                f' (updated >= {str_from} AND updated <= {str_to}))',
                startAt=start_at,
            )
        return IssueIterator(_internal, self.jira.issue)


    def dump(self, issues, output):
        if not os.path.exists(output):
            os.makedirs(output)
        for issue in issues:
            print(f"writting {issue.key}")
            with open(os.path.join(output, f'{issue.key}.yaml'), 'w+') as fd:
                yaml.dump(issue.raw, fd, default_flow_style=False)


