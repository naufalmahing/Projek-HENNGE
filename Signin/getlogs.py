import requests

def get_logs(access_token, user_name):
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get('https://dev-onwaezps.jp.auth0.com/api/v2/logs?q=user_name%3A' + user_name, headers=headers)
    return response._content