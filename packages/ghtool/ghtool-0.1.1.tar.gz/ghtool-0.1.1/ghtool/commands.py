import requests
import grequests

BASE_GITHUB_API_ENDPOINT = 'https://api.github.com/'

class Command:
    def __init__(self, args):
        self.args = args

    def execute(self): pass

    @staticmethod
    def name(): pass

class ListCommand(Command):
    def execute(self):
        url = BASE_GITHUB_API_ENDPOINT + 'search/repositories'
        payload = {}
        payload['per_page'] = self.args.n
        payload['page'] = 1
        payload['order'] = 'desc'
        payload['sort'] = 'updated'
        if self.args.language:
            payload['q'] = 'language:' + self.args.language
        else:
            payload['q'] = 'private:false'
        res = requests.get(url, params=payload)
        repos = res.json()['items']
        for rep in repos:
            print(rep['name'] + ' ' + rep['language'])

    @staticmethod
    def name():
        return 'list'

class DescCommand(Command):
    def execute(self):
        base_url = BASE_GITHUB_API_ENDPOINT + 'repositories/'
        rs = (grequests.get(base_url+repo_id) for repo_id in self.args.repo_ids)
        rss = grequests.map(rs)
        print('{0:20}{1:20}{2:20}{3}'.format('name', 'owner', 'language', 'html_url'))
        for r in rss:
            item = r.json()
            print('{0:20}{1:20}{2:20}{3}'.format(item['name'], item['owner']['login'], item['language'], item['html_url']))

    @staticmethod
    def name():
        return 'desc'


