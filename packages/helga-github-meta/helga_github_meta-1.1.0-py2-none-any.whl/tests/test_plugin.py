import json
import sys
import unittest
try:
    from unittest import mock
except ImportError:
    from mock import mock
# kinda nasty hack since helga doesnt support py3 :(
sys.modules['helga.plugins'] = mock.Mock()
from helga_github_meta import plugin


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = json.dumps(content)
            self.status_code = status_code

        def json(self):
            return self.content

    if 'issues' in args[0]:
        return MockResponse({
            'title': 'title1',
            'state': 'closed',
            'updated_at': '2016-05-18T02:09:24Z',
        }, 200)
    elif 'repos' in args[0]:
        return MockResponse({
            'name': 'name1',
            'description': 'description1',
            'updated_at': '2016-05-18T02:09:24Z',
        }, 200)
    elif 'users' in args[0]:
        return MockResponse({
            'name': 'name1',
            'company': 'company1',
            'blog': 'narfman0.example.com',
            'email': 'narfman0@example.com',
            'public_repos': '1337',
        }, 200)
    return MockResponse({}, 404)


class TestPlugin(unittest.TestCase):
    @mock.patch('helga_github_meta.plugin.requests.get', side_effect=mocked_requests_get)
    def test_issues(self, mock_get):
        response = plugin.meta_issue('/narfman0/test1/issues/1')
        self.assertTrue('title1' in response)
        self.assertTrue('closed' in response)
        self.assertTrue('ago' in response)

    @mock.patch('helga_github_meta.plugin.requests.get', side_effect=mocked_requests_get)
    def test_repo(self, mock_get):
        response = plugin.meta_repo('/narfman0/test1')
        self.assertTrue('name1' in response)
        self.assertTrue('description1' in response)
        self.assertTrue('ago' in response)

    @mock.patch('helga_github_meta.plugin.requests.get', side_effect=mocked_requests_get)
    def test_user(self, mock_get):
        response = plugin.meta_user('/narfman0')
        self.assertTrue('name1' in response)
        self.assertTrue('company1' in response)
        self.assertTrue('narfman0.example.com' in response)
        self.assertTrue('narfman0@example.com' in response)
        self.assertTrue('1337' in response)


if __name__ == '__main__':
    unittest.main()
