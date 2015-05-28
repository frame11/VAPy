import datetime, re, requests
from functools import wraps
try:
        import ujson as json
except:
        import json

import Profiles

API_URL = 'https://fakevout.azurewebsites.net/api/v1/'
TOKEN_URL = 'https://fakevout.azurewebsites.net/api/token'



class VAPy:
    
    def __init__(self):
        self.headers = {}

    # HELPER FUNCTIONS

    def get_token(self, uname, pwd, api_key):
        temp_header = {'Voat-ApiKey': api_key, 'Content-Type': 'application/json'}
        body = 'grant_type=password&username={}&password={}'.format(uname,pwd)
        r = requests.post(TOKEN_URL, headers=temp_header, data=body)
        r.connection.close()
        resp =  json.loads(r.content)
        if 'error' not in resp.keys():
            return resp['access_token']
        else:
            return False
    
    def set_headers(self, uname, pwd, api_key, api_token):
        self.headers = {'Voat-ApiKey':api_key,'Authorization':'Bearer '+api_token,'Content-Type':'application/json'}

    def load_profile(self, profile, pwd):
        profiles = Profiles.Profiles()
        res = profiles.get_profile(profile, pwd)
        self.set_headers(res[0], res[1], res[2], res[3])

    def querystring(search='', count=50):
        return '?search={}&count={}'.format(search, count)

    def parse_bad_request(self, result):
        if result['success']:
            print("Cannot parse error for successful request. No error to parse.")
            return None
        else:
            print(result)

    # WRAPPERS

    def catch_empty_input(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except (KeyError, TypeError):
                return None
        return wrapper
    
    def catch_empty_filter_input(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return(func(self, *args, **kwargs))
            except (KeyError, TypeError):
                return False
        return wrapper

    def check_input_is_submission(func):
        @wraps(func)
        def wrapper(self, inp):
            if self.is_submission(inp):
                return func(self, inp)
            else:
                raise ValueError('{} requires a submission dict as an argument.'.format(func.__name__))
        return wrapper

    def check_input_is_comment(func):
        @wraps(func)
        def wrapper(self, inp):
            if self.is_comment(inp):
                return func(self, inp)
            else:
                raise ValueError('{} requires a comment dic'.format(func.__name__))
        return wrapper

    def check_response(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            return result['data'] if result['success'] == True else self.parse_bad_request(result)
        return wrapper

    # VOAT CONTENT GETTERS

    def get_subverse(self, subverse):
        submissions = self.get_submissions_by_subverse(subverse)
        return [(submission, self.get_comments_by_submission(submission)) for submission in submissions]

    @check_response
    def get_submission_by_id(self, subverse, submission_id):
        url = API_URL + 'v/{}/{}'.format(subverse, submission_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp

    @check_response
    def get_submissions_by_subverse(self, subverse):
        url = API_URL + 'v/{}'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp

    def get_content_submissions_by_subverse(self, subverse):
        return filter(self.is_content_submission, self.get_submissions_by_subverse(subverse))

    def get_url_submissions_by_subverse(self, subverse):
        return filter(self.is_url_submission, self.get_submissions_by_subverse(subverse))

    @check_response
    def get_comment_by_id(self, comment_id):
        url = API_URL + 'comments/{}'.format(comment_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp
    
    @check_response
    def get_comments_by_submission(self, submission, subverse=None):
        #url = ""
        if type(submission) == int:
            url = API_URL + 'v/{}/{}/comments'.format(subverse, submission)
        elif type(submission) == dict:
            url = API_URL + 'v/{}/{}/comments'.format(self.get_subverse_name(submission), self.get_id(submission))
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp

    # SUBVERSE INFO FUNCTIONS

    def subverse_info(self, subverse):
        url = API_URL + 'v/{}/info'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    @catch_empty_input
    def get_subverse_creation_date(self, subverse):
        return self.subverse_info(subverse)['creationDate']

    @catch_empty_input
    def get_subverse_subscriber_count(self, subverse):
        return int(self.subverse_info(subverse)['subscriberCount'])
    
    @catch_empty_input
    def get_subverse_rated_adult(self, subverse):
        return self.subverse_info(subverse)['ratedAdult']
    
    @catch_empty_input
    def get_subverse_sidebar(self, subverse):
        return self.subverse_info(subverse)['sidebar']
    
    # USER INFO FUNCTIONS

    def user_info(self, user):
        url = API_URL + 'u/{}/info'.format(user)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}


    # POST

    @check_response
    def post_text_submission(self, subverse, title, text):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'content':text})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def post_link_submission(self, subverse, title, url):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'url':url})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def post_reply_to_submission(self, submission_id, comment):
        subverse = self.get_subverse_name(self.get_submission_by_id(submission_id))
        url = API_URL + 'v/{}/{}/comment'.format(subverse, submission_id)
        body = json.dumps({'value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def post_reply_to_comment(self, comment_id, comment):
        submission_id = self.get_comment_submission(self.get_comment_by_id(comment_id))
        subverse = self.get_subverse_name(self.get_submission_by_id(submission_id))
        url = API_URL + 'v/{}/{}/comment/{}'.format(subverse, submission_id, comment_id)
        body = json.dumps({'value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def post_reply_to_pm(self, pm_id, comment):
        url = API_URL + 'comments/{}'.format(pm_id)
        body = json.dumps({'value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    # EDIT CONTENT

    @check_response
    def edit_submission(self, submission_id, title, content):
        submission = self.get_submission_by_id(submission_id)
        subverse, s_type = self.get_subverse_name(submission), self.get_submission_type(submission)
        url = API_URL + 'v/{}/{}'.format(subverse, submission_id)
        body = json.dumps({'title':title,s_type:content})
        r = requests.put(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def edit_comment(self, comment_id, comment):
        url = API_URL + 'comments/{}'.format(comment_id)
        body = json.dumps({'value':comment})
        r = requests.put(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp


    # DELETE CONTENT

    @check_response
    def delete_submission(self, submission_id, title, content):
        submission = self.get_submission_by_id(submission_id)
        subverse = self.get_subverse_name(submission)
        url = API_URL + 'v/{}/{}'.format(subverse, submission_id)
        r = requests.delete(url, headers=self.headers)
        resp = json.loads(r.text)
        r.connection.close()
        return resp

    @check_response
    def delete_comment(self, comment_id, comment):
        url = API_URL + 'comments/{}'.format(comment_id)
        r = requests.delete(url, headers=self.headers)
        resp = json.loads(r.text)
        r.connection.close()
        return resp



    # VOTE

    #def 


    # VOAT DICT FUNCS
    
    def get_content(self, voat_dict, ignore_links=False):
        if ignore_links == True:
            return voat_dict['content']
        elif ignore_links == False:
            if self.is_url_submission(voat_dict):
                return voat_dict['url']
            else:
                return voat_dict['content']

    '''
    @catch_empty_input
    def get_subverse_name(self, voat_dict):
        if self.is_submission(voat_dict):        
            return voat_dict['subverse']
        else:
            submission_id = self.get_comment_submission(voat_dict)
            return self.get_subverse_name(self.get_submission
            #return self.get_subverse(self.submission_from_id(submission_id))

            return self.get_submission_by_id(submission_id)['subverse']
    '''

    def get_author(self, voat_dict):
        return voat_dict['userName']

    def get_scores(self, voat_dict):
        return voat_dict['upVotes'], voat_dict['downVotes']

    def get_score(self, voat_dict):
        up, down = self.get_scores(voat_dict)
        return up - down

    def get_date(self, voat_dict):
        # split used to remove partial seconds
        return datetime.strptime(voat_dict['date'].split(".")[0], "%Y-%m-%dT%H:%M:%S")


        return voat_dict['date']

    @catch_empty_input
    def get_id(self, voat_dict):
        return voat_dict['id']

    @catch_empty_input
    def get_permalink(self, voat_dict):
        if self.is_submission(voat_dict):
            return "https://fakevout.azurewebsites.net/v/{}/comments/{}".format(
                    self.get_subverse(voat_dict), self.get_id(voat_dict))

    # SUBMISSION DICT FUNCS

    @check_input_is_submission
    def get_submission_type(self, submission_dict):
        return 'content' if submission_dict['type'] == 1 else 'url'

    @catch_empty_input
    def get_submission_title(self, submission_dict):
        return submission_dict['title']

    @catch_empty_input
    def get_submission_rank(self, submission_dict):
        return float(submission_dict['rank'])

    @catch_empty_input
    def get_submission_comment_count(self, submission_dict):
        return int(submission_dict['commentCount'])

    # COMMENT DICT FUNCS

    @catch_empty_input
    def get_comment_submission(self, comment_dict):
        return comment_dict['submissionID']

    def get_parent_id(self, comment_dict):
        return comment_dict['parentID']

    # FILTERS

    def is_submission(self, voat_dict):
        return True if 'type' in voat_dict.keys() else False

    def is_comment(self, voat_dict):
        return True if 'parentID' in voat_dict.keys() else False

    def is_content_submission(self, submission_dict):
        return True if self.get_submission_type(submission_dict) == 'content' else False

    def is_url_submission(self, submission_dict):
        return True if self.get_submission_type(submission_dict) == 'url' else False

    def contains_regex(self, regex, voat_dict, ignore_links=False):
        if ignore_links == False:
            return True if ( self.contains_regex_in_title(regex, voat_dict) or self.contains_regex_in_content(regex, voat_dict) ) else False
        else:
            return True if ( self.contains_regex_in_title(regex, voat_dict) or self.contains_regex_in_content(regex, voat_dict, ignore_links=True) ) else False

    @catch_empty_filter_input   
    def contains_regex_in_title(self, regex, submission_dict):
        return bool(re.search(regex, self.get_submission_title(submission_dict))) 
   
    @catch_empty_filter_input
    def contains_regex_in_content(self, regex, voat_dict, ignore_links=False):
        return bool(re.search(regex, self.get_content(voat_dict, ignore_links=ignore_links)))
   
    @catch_empty_filter_input
    def contains_regex_in_link(self, regex, submission_dict):
        return bool(re.search(regex, self.get_content(submission_dict)))

    @catch_empty_filter_input
    def is_top_level_comment(self, comment_dict):
        return bool(comment_dict['parentID'])



