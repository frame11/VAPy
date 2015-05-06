import requests

try:
        import ujson as json
except:
        import json



TOKEN_URL = 'https://fakevout.azurewebsites.net/api/token'



class VAPy:
    
    def __init__(self, api_key, uname, pwd):
        self.headers = {'Voat-ApiKey': api_key}
        token = self.get_token(api_key, uname, pwd)
        self.headers['Authorization'] = 'Bearer {}'.format(token)

    def get_token(self, api_key, uname, pwd):
        body = 'grant_type=password&username={}&password={}'.format(uname,pwd)
        r = requests.post(TOKEN_URL, headers=self.headers, data=body)
        resp =  json.loads(r.content)
        return resp['access_token']
