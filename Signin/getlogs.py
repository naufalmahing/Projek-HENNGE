import requests

def get_logs(access_token, user_name):
    print('get_' + 'logs')
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get('https://dev-onwaezps.jp.auth0.com/api/v2/logs?q=user_name%3A' + user_name, headers=headers)

    print(type(response))
    print(response)
    print(response._content)
    return response._content