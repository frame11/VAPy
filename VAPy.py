import requests

try:
        import ujson as json
except:
        import json


API_URL = 'https://fakevout.azurewebsites.net/api/v1/'
TOKEN_URL = 'https://fakevout.azurewebsites.net/api/token'



class VAPy:
    
    def __init__(self, api_key, uname, pwd):
        self.headers = {'Voat-ApiKey': api_key}
        token = self.get_token(api_key, uname, pwd)
        if token != False:
            self.headers['Authorization'] = 'Bearer {}'.format(token)

    def get_token(self, api_key, uname, pwd):
        body = 'grant_type=password&username={}&password={}'.format(uname,pwd)
        r = requests.post(TOKEN_URL, headers=self.headers, data=body)
        resp =  json.loads(r.content)
        if 'error' not in resp.keys():
            return resp['access_token']
        else:
            return False



    # SUBVERSE FUNCTIONS

    def subverse_info(self, subverse):
        url = API_URL + "v/{}/info".format(subverse)
        r = requests.get(url, headers=self.headers) 
        return json.loads(r.content)

    def get_subverse_creation_date(self, subverse):
        return self.subverse_info(subverse)["creationDate"]

    def get_subverse_subscriber_count(self, subverse):
        return int(self.subverse_info(subverse)["subscriberCount"])

    def get_subverse_rated_adult(self, subverse):
        return True if self.subverse_info(subverse)["ratedAdult"] == "true" else False

    def get_subverse_sidebar(self, subverse):
        return self.subverse_info(subverse)["sidebar"]
