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

    def check_empty_input(func):
        def wrapper(self, inp):
            try:
                return(func(self, inp))
            except KeyError:
                return {}
        return wrapper

    def check_input_is_submission(func):
        def wrapper(self, inp):
            if self.is_submission(inp):
                return func(self, inp)
            else:
                raise ValueError('You are calling a submission-only method on something that is not a submission')

    def check_input_is_comment(func):
        def wrapper(self, inp):
            if self.is_comment(inp):
                return func(self, inp)
            else:
                raise ValueError('You are calling comment-only methods on something that is not a comment')

    def querystring(search='', count=50):
        return '?search={}&count={}'.format(search, count)

    # SUBVERSE INFO FUNCTIONS

    def subverse_info(self, subverse):
        url = API_URL + 'v/{}/info'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    @check_empty_input
    def get_subverse_creation_date(self, subverse):
        return self.subverse_info(subverse)['creationDate']

    @check_empty_input
    def get_subverse_subscriber_count(self, subverse):
        return int(self.subverse_info(subverse)['subscriberCount'])
    
    @check_empty_input
    def get_subverse_rated_adult(self, subverse):
        return self.subverse_info(subverse)['ratedAdult']
    
    @check_empty_input
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
        body = json.dumps({'Value':comment})
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

    @check_empty_input
    def get_submission_type(self, submission_dict):
        return 'content' if submission_dict['type'] == 1 else 'url'

    @check_empty_input
    def get_content(self, submission_dict):
        if submission_dict != {}:
            return submission_dict[self.get_submission_type(submission_dict)]
        else:
            return {}
    
    @check_empty_input
    def get_submission_subverse(self, submission_dict):
        return submission_dict['subverse']

    @check_empty_input
    def get_submission_title(self, submission_dict):
        return submission_dict['title']

    @check_empty_input
    def get_submission_author(self, submission_dict):
        return submission_dict['userName']

    @check_empty_input
    def get_submission_scores(self, submission_dict):
        return submission_dict['upVotes'], submission_dict['downVotes']

    @check_empty_input
    def get_submission_score(self, submission_dict):
        if submission_dict != {}:
            up, down = self.get_submission_scores(submission_dict)
            return up - down
        else:
            return {}

    @check_empty_input
    def get_submission_date(self, submission_dict):
        return submission_dict['date']

    @check_empty_input
    def get_submission_rank(self, submission_dict):
        return float(submission_dict['rank'])

    @check_empty_input
    def get_submission_comment_count(self, submission_dict):
        return int(submission_dict['commentCount'])


    # FILTERS

    def is_submission(self, voat_dict):
        return True if 'type' in voat_dict.keys() else False

    def is_comment(self, voat_dict):
        return True if 'parentID' in voat_dict.keys() else False

    def is_content_submission(self, submission_dict):
        return True if self.get_submission_type == 'content' else False

    def is_url_submission(self, submission_dict):
        return True if self.get_submission_type == 'url' else False

    def contains_regex(self, voat_dict, regex, search_link=False):
        if search_link == False:
            return True if ( self.contains_regex_in_title(voat_dict, regex) OR
                             self.contains_reges_in_content(voat_dict
    
    @check_input_is_submission
    def contains_regex_in_title(self, submission_dict, regex):
        return bool(re.search(regex, self.get_submission_title(submission_dict))) 
    
    def contains_regex_in_content(self, 
    
    
    # COMMENT GETTERS

    def comment_dict_from_id(self, comment_id):
        url = 'comments/{}'.format(comment_id)
        r = requests.get(url, headers=self.headers)
        resp = json.dumps(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    @check_empty_input
    def get_comment_subverse(self, comment_dict)
        return comment_dict['submissionID']

   @check_empty_input
    def get_comment_scores(self, comment_dict):
        return comment_dict['upVotes'], commenet_dict['downVotes']

    @check_empty_input
    def get_comment_score(self, comment_dict):
        if comment_dict != {}:
            up, down = self.get_comment_scores(comment_dict)
            return up - down
        else:
            return {}

    @check_empty_input
    def get_comment_author(self, comment_dict):
        return comment_dict['userName']
