import json
from user import User
from urllib.parse import urlparse
import http.client


class Client:
    _muUrl = ''
    _muKey = ''

    def __init__(self, mu_url, mu_key):
        self._muUrl = mu_url
        self._muKey = mu_key

    def _gen_users_url(self):
        url = self._muUrl + "/users"
        return url

    def _gen_user_url(self, user_id):
        url = self._muUrl + "/users/" + user_id
        return url

    def _gen_headers(self):
        headers = {
            'Token': self._muKey
        }
        return headers

    def get_url(self):
        return self._muUrl

    def new_user(self):
        user = User
        user.update_traffic(user)

    def get_users_res(self):
        url = self._gen_users_url()
        o = urlparse(url)

        conn = http.client.HTTPConnection(o.netloc)
        headers = self._gen_headers()
        conn.request("GET", o.path, headers=headers)

        res = conn.getresponse()
        data = res.read()
        return data.decode('utf-8')
