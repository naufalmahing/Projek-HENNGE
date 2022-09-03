import requests
# import http.client
import chetchet

def send(access_token):
    headers = { 'authorization': "Bearer " + access_token }

    response = requests.get('https://dev-onwaezps.jp.auth0.com/api/v2/logs?q=user_name%3Anopal*', headers=headers)

    print('this is me' + ', hello there')
    print(type(response))
    print(response)
    print(response._content)

send(chetchet.get_token()['access_token'])