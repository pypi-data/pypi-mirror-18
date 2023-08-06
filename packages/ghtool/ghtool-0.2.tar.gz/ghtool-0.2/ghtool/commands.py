'''
This module contains all commands for consuming GitHub API endpoints.
Commands are basic simple implementation of Command design pattern.
There are also helper method for building queries and method for
finding last repository on GitHub.
'''
import requests
import grequests
import time

BASE_GITHUB_API_ENDPOINT = 'https://api.github.com/'
DEFAULT_NUM_OF_REPOS = 10


def find_last_repo(l, r):
    '''
    This method is simple implementation of bin search with purpose
    to find last repository.
    It takes two parameters: left and right boundary (integers).
    Method returns id of last repository.
    '''
    # TODO: add some restrictions, for example: must l < r (otherwise raise exception), also cover http errors
    since = (l + r) // 2
    res = requests.get(BASE_GITHUB_API_ENDPOINT + 'repositories', params={'since': since})
    repos = res.json()
    cnt = len(repos)
    if cnt == 0:
        return find_last_repo(l, since)
    elif cnt == 100:
        return find_last_repo(since, r)
    else:
        return repos[cnt-1]['id']

def q_builder(args):
    '''
    This method builds q param for search.
    It takes args and returns built query string.
    '''
    # TODO: extend builder for more args
    s = ' '.join(args.word)
    if args.language: s += '+language:' + args.language
    return s

class Command:
    '''
    This is base class for implementation of Command
    design pattern with all methods that should be
    overridden in subclasses.
    '''
    def __init__(self, args):
        self.args = args

    def execute(self):
        '''
        This method should have implementation of execution logic
        for specific command.
        '''
        pass

    @staticmethod
    def name():
        '''
        This method should return name of specific command.
        '''
        pass

    @staticmethod
    def add_cmd_subparser(subparsers):
        '''
        This method should add subcommand parser to passed subarsers object.
        '''
        pass


# class ListCommand(Command):
#     def execute(self):
#         url = BASE_GITHUB_API_ENDPOINT + 'search/repositories'
#         last_id = find_last_repo(72000000, 100000000)
#         # TODO: depends on -n arg, fetch another set of repositories
#         # problem: rate limit
#
#     @staticmethod
#     def name():
#         return 'list'
#
#     @staticmethod
#     def add_cmd_subparser(subparsers):
#         parser = subparsers.add_parser('list', help='list help')
#         parser.add_argument('language', help='programming language', nargs='?')
#         parser.add_argument('-n', type=int,
#                             help='number of repositories to show (DEFAULT: {})'.format(DEFAULT_NUM_OF_REPOS),
#                             default=DEFAULT_NUM_OF_REPOS)


class DescCommand(Command):
    def execute(self):
        base_url = BASE_GITHUB_API_ENDPOINT + 'repositories/'
        rs = (grequests.get(base_url + repo_id) for repo_id in self.args.repo_ids)
        # TODO: add error handling
        responses = grequests.map(rs)
        print('{0:20}{1:20}{2:20}{3}'.format('name', 'owner', 'language', 'html_url'))
        for r in responses:
            if r.status_code == 200:
                item = r.json()
                print('{0:20}{1:20}{2:20}{3}'.format(item['name'], item['owner']['login'], item['language'],
                                                     item['html_url']))

    @staticmethod
    def name():
        return 'desc'

    @staticmethod
    def add_cmd_subparser(subparsers):
        parser = subparsers.add_parser('desc', help='description of repositories')
        parser.add_argument('repo_ids', help='Language help', nargs='*')


class SearchCommand(Command):
    MAP_SORTOPT_TO_PROP = {
        'stars': 'stargazers_count',
        'updated': 'updated_at',
        'forks': 'forks_count'
    }

    def execute(self):
        url = BASE_GITHUB_API_ENDPOINT + 'search/repositories'
        payload = {'per_page': self.args.per_page, 'page': self.args.page,
                   'order': self.args.order, 'sort': self.args.sort,
                   'q': q_builder(self.args)}
        try:
            res = requests.get(url, params=payload)
        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))
            return

        if res.status_code == 200:
            repos = res.json()['items']
            print('{0:<20} {1}'.format(self.args.sort, 'full_name'))
            for repo in repos:
                print('{0:<20} {1}'.format(repo[SearchCommand.MAP_SORTOPT_TO_PROP[self.args.sort]], repo['full_name']))

    @staticmethod
    def name():
        return 'search'

    @staticmethod
    def add_cmd_subparser(subparsers):
        parser = subparsers.add_parser('search', help='search repositories')
        parser.add_argument('word', help='search word', nargs='+')
        parser.add_argument('-language', help='programming language', nargs='?')
        parser.add_argument('-per_page', type=int,
                            help='number of repositories per page (DEFAULT: {})'.format(DEFAULT_NUM_OF_REPOS),
                            default=DEFAULT_NUM_OF_REPOS)
        parser.add_argument('-page', type=int,
                            help='page (DEFAULT: 1)',
                            default=1)
        parser.add_argument('-sort', help='sort by field (DEFAULT: \'stars\')', default='stars',
                            choices=['stars', 'forks', 'updated'])
        parser.add_argument('-order', help='sort order (DEFAULT: \'desc\')', default='desc', choices=['desc', 'asc'])

class LastRepoCommand(Command):
    def execute(self):
        start = time.time()
        print('Last repo id: {}'.format(find_last_repo(72000000, 100000000)))
        end = time.time()
        print('Elapsed time: {}'.format(end - start))

    @staticmethod
    def name():
        return 'last_repo'

    @staticmethod
    def add_cmd_subparser(subparsers):
        subparsers.add_parser('last_repo', help='find last repository')
