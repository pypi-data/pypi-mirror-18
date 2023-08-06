import requests
import simplejson


class Client:
    _muUrl = ''
    _muKey = ''
    _nodeId = 1

    def __init__(self, mu_url, node_id, mu_key):
        self._muUrl = mu_url
        self._nodeId = node_id
        self._muKey = mu_key

    def _gen_users_url(self):
        return "{0}/nodes/{1}/users".format(self._muUrl, self._nodeId)

    def _gen_node_traffic_url(self):
        return "{0}/nodes/{1}/traffic".format(self._muUrl, self._nodeId)

    def _gen_headers(self):
        headers = {
            'Token': self._muKey
        }
        return headers

    def get_url(self):
        return self._muUrl

    def gen_traffic_log(self, user_id, u, d):
        return {
            "user_id": user_id,
            "u": u,
            "d": d,
        }

    def update_traffic(self, data):
        uri = self._gen_node_traffic_url()
        r = requests.post(uri, json=data, headers=self._gen_headers())
        if r.status_code != 200:
            return False
        return True

    def get_users_res(self):
        r = requests.get(self._gen_users_url(), headers=self._gen_headers())
        if r.status_code != 200:
            return None
        return r.json()['data']
