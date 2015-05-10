import requests

try:
        import ujson as json
except:
        import json


API_URL = 'https://fakevout.azurewebsites.net/api/v1/'
TOKEN_URL = 'https://fakevout.azurewebsites.net/api/token'



class VAPy:
    
    def __init__(self, api_key, uname, pwd):
        self.headers = {'Voat-ApiKey': api_key, 'Content-Type': 'application/json'}
        token = self.get_token(api_key, uname, pwd)
        if token != False:
            #self.headers['Authorization'] = 'Bearer {}'.format(token)
            self.headers = {'Voat-ApiKey':api_key,'Authorization':'Bearer '+token,'Content-Type':'application/json'}

    # HELPER FUNCTIONS

    def get_token(self, api_key, uname, pwd):
        body = 'grant_type=password&username={}&password={}'.format(uname,pwd)
        r = requests.post(TOKEN_URL, headers=self.headers, data=body)
        r.connection.close()
        resp =  json.loads(r.content)
        if 'error' not in resp.keys():
            return resp['access_token']
        else:
            return False

    def validate_input(func):
        def wrapper(self, inp):
            try:
                return(func(self, inp))
            except KeyError:
                return {}
        return wrapper

    def querystring(search='', count=50):
        return '?search={}&count={}'.format(search, count)

    # SUBVERSE INFO FUNCTIONS

    def subverse_info(self, subverse):
        url = API_URL + 'v/{}/info'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    @validate_input
    def get_subverse_creation_date(self, subverse):
        return self.subverse_info(subverse)['creationDate']

    @validate_input
    def get_subverse_subscriber_count(self, subverse):
        return int(self.subverse_info(subverse)['subscriberCount'])
    
    @validate_input
    def get_subverse_rated_adult(self, subverse):
        return self.subverse_info(subverse)['ratedAdult']
    
    @validate_input
    def get_subverse_sidebar(self, subverse):
        return self.subverse_info(subverse)['sidebar']
    
    # FIND


    # POST

    def post_text_submission(self, subverse, title, text):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'content':text})
        r = requests.post(url, headers=self.headers, data=body)
        r.connection.close()

    def post_link_submission(self, subverse, title, url):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'url':url})
        r = requests.post(url, headers=self.headers, data=body)
        r.connection.close()

    def post_reply_to_submission(self, submission_id, comment):
        subverse = self.get_submission_subverse(submission_id)
        url = API_URL + 'v/{}/{}/comment'.format(subverse, submission_id)
        body = json.dumps({'Value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        r.connection.close()

    def post_reply_to_comment(self, comment_id, comment):
        submission_id = self.get_comment_submission(self.comment_dict_from_id(comment_id))
        subverse = self.get_submission_sibverse(self.submission_dict_from_id(submission_id))
        url = API_URL + 'v/{}/{}/comment/{}'.format(subverse, submission_id, comment_id)
        body = json.dumps({'Value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        r.connection.close()

    def post_reply_to_pm(self, pm_id, comment):
        url = API_URL + 'comments/{}'.format(pm_id)
        body = json.dumps('Value':comment)
        r = requests.post(url, headers=self.headers, data=body)
        r.connection.close()
    
    # SUBMISSION GETTERS

    def submission_dict_from_id(self, submission_id):
        url = API_URL + 'submissions/{}'.format(submission_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    def submission_dicts_from_subverse(self, subverse):
        url = API_URL + 'v/{}'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else []

    @validate_input
    def get_submission_type(self, submission_dict):
        return 'formattedContent' if submission_dict['type'] == 1 else 'url'

    @validate_input
    def get_submission_content(self, submission_dict):
        if submission_dict != {}:
            return submission_dict[self.get_submission_type(submission_dict)]
        else:
            return {}
    
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
        if submission_dict != {}:
            up, down = self.get_submission_scores(submission_dict)
            return up - down
        else:
            return {}

    @validate_input
    def get_submission_date(self, submission_dict):
        return submission_dict['date']

    @validate_input
    def get_submission_rank(self, submission_dict):
        return float(submission_dict['rank'])

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
        resp = json.dumps(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    @validate_input
    def get_comment_subverse(self, comment_dict)
        return comment_dict['submissionID']

   @validate_input
    def get_comment_scores(self, comment_dict):
        return comment_dict['upVotes'], commenet_dict['downVotes']

    @validate_input
    def get_comment_score(self, comment_dict):
        if comment_dict != {}:
            up, down = self.get_comment_scores(comment_dict)
            return up - down
        else:
            return {}

    @validate_input
    def get_comment_author(self, comment_dict):
        return comment_dict['userName']
