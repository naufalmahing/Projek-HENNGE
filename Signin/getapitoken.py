import http.client
import json
from django.conf import settings

def get_api_token():
    conn = http.client.HTTPSConnection("dev-onwaezps.jp.auth0.com")

    payload = "{\"client_id\":\"YNqCStmO4umXgq0WGrHNArweJKyerBdz\",\"client_secret\":\"Yqqy3ugZC3jRYVXuKhzfPgfIWeHm0nyPUh25_mWMEaMRIV505R3BhihfYy0Cxfh_\",\"audience\":\"https://dev-onwaezps.jp.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data)
    return data