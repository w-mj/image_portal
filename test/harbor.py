import datetime
import os
from urllib.parse import urljoin, quote, urlencode

import requests


class Client(requests.Session):
    def __init__(self, base_url="https://docker.educg.net/api/v2.0/"):
        super().__init__()
        self.base_url = base_url
        user = os.environ['USER']
        password = os.environ['PASS']
        self.auth = (user, password)

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)

    def page(self, url: str, **kwargs):
        page = 1
        if kwargs.get('params') is None:
            kwargs['params'] = {}
        while True:
            kwargs['params']['page'] = page
            kwargs['params']['page_cnt'] = 10
            ans = self.get(url, **kwargs)
            if not 200 <= ans.status_code < 300:
                print(ans.json())
                return
            ans = ans.json()
            if not ans:
                break
            for i in ans:
                yield i
            page += 1


def get_artifacts(proj, repo):
    ans = []
    repo = repo.replace(proj + "/", "")
    repo_url = repo.replace('/', '%252F')
    for arti in Client().page(f"projects/{quote(proj)}/repositories/{repo_url}/artifacts", params={
        'with_tag': 'true',
        'with_label': 'false',
        'with_scan_overview': 'false',
        'with_signature': 'false',
        'with_immutable_status': 'false',
        'with_accessory': 'false'
    }):
        for t in arti['tags']:
            push_time = datetime.datetime.strptime(t['push_time'], "%Y-%m-%dT%H:%M:%S.%f%z")
            ans.append((t['name'], push_time))
    ans = sorted(ans, key=lambda x: x[1])
    return ans[-1][0]


def get_repos(proj):
    for repo in Client().page(f"projects/{proj}/repositories"):
        tag = get_artifacts(proj, repo['name'])
        print(repo['name'] + ":" + tag)

def get_projs():
    for proj in Client().page("projects", params={"with_detail": "false"}):
        print(proj['name'])
        get_repos(proj['name'])


if __name__ == '__main__':
    # get_projs()
    get_repos('ai4s')
    # get_artifacts('ai4s', 'ai4s/vnc/ubuntu20.04-test')