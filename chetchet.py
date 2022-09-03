import http.client
# from Signin import getlogs
import json

def get_token():
    conn = http.client.HTTPSConnection("dev-onwaezps.jp.auth0.com")

    payload = "{\"client_id\":\"YNqCStmO4umXgq0WGrHNArweJKyerBdz\",\"client_secret\":\"Yqqy3ugZC3jRYVXuKhzfPgfIWeHm0nyPUh25_mWMEaMRIV505R3BhihfYy0Cxfh_\",\"audience\":\"https://dev-onwaezps.jp.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    data = data.decode("utf-8")
    print(type(data))
    data = json.loads(data)
    print(type(data))
    return data