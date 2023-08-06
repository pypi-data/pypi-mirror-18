import user, client
import json

url = 'http://sp3.dev/mu/v2'
key = 'abc'

client = client.Client(url, key)
json_str = client.get_users_res()
data = json.loads(json_str)
print(data['data'])
