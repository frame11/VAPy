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


    def validate_input(func):
        def wrapper(self, inp):
            try:
                return(func(self, inp))
            except TypeError:
                return False
        return wrapper

    # SUBVERSE INFO FUNCTIONS

    def subverse_info(self, subverse):
        url = API_URL + 'v/{}/info'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        return resp['data'] if resp['success'] == True else False

    @validate_input
    def get_subverse_creation_date(self, subverse):
        return self.subverse_info(subverse)['creationDate']

    @validate_input
    def get_subverse_subscriber_count(self, subverse):
        return int(self.subverse_info(subverse)['subscriberCount'])
    
    @validate_input
    def get_subverse_rated_adult(self, subverse):
        return 'unrated' if self.subverse_info(subverse)['ratedAdult'] == False else 'rated'
    
    @validate_input
    def get_subverse_sidebar(self, subverse):
        return self.subverse_info(subverse)['sidebar']

    # SUBMISSION GETTERS

    def submission_dict_from_id(self, submission_id):
        url = API_URL + 'submissions/{}'.format(submission_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        return resp['data'] if resp['success'] == True else False

    def get_subverse_submissions(self, subverse):
        url = API_URL + 'v/{}'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        return resp

    @validate_input
    def get_submission_type(self, submission_dict):
        return 'formattedContent' if submission_dict['type'] == 1 else 'url'

    @validate_input
    def get_submission_content(self, submission_dict):
        return submission_dict[self.get_submission_type(submission_dict)]

    @validate_input
    def get_submission_subverse(self, submission_dict):
        return submission_dict['subverse']

    @validate_input
    def get_submission_title(self, submission_dict):
        return submission_dict['title']

    @validate_input
    def get_submission_author(self, submission_dict):
        return submission_dict['userName']

    @validate_input
    def get_submission_scores(self, submission_dict):
        return submission_dict['upVotes'], submission_dict['downVotes']

    @validate_input
    def get_submission_score(self, submission_dict):
        up, down = self.get_submission_scores(submission_dict)
        return up - down

    @validate_input
    def get_submission_date(self, submission_dict):
        return submission_dict['date']

    @validate_input
    def get_submission_ranl(self, submission_dict):
        return submission_dict['rank']

    @validate_input
    def get_submission_comment_count(self, submission_dict):
        return int(submission_dict['commentCount'])


    # SUBMISSION FILTERS

    def submission_is_text(self, submission_dict):
        return True if self.get_submission_type == 'text' else False

    def submission_is_link(self, submission_dict):
        return True if self.get_submission_type == 'link' else False


    # COMMENT GETTERS

    def comment_dict_from_id(self, comment_id):
        url = 'comments/{}'.format(comment_id)
        r = requests.get(url, headers=self.headers)
    

