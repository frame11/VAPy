import re, requests

try:
        import ujson as json
except:
        import json

import Profiles

API_URL = 'https://fakevout.azurewebsites.net/api/v1/'
TOKEN_URL = 'https://fakevout.azurewebsites.net/api/token'



class VAPy:
    
    def __init__(self):
        pass

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


    # WRAPPERS

    def catch_empty_input(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                return result if type(result) != None else {}
            except (KeyError, TypeError):
                return {}
        return wrapper
    
    def catch_empty_filter_input(func):
        def wrapper(self, *args, **kwargs):
            try:
                return(func(self, *args, **kwargs))
            except (KeyError, TypeError):
                return False
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
    
    # FIND


    # POST

    def post_text_submission(self, subverse, title, text):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'content':text})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp['data']['id']

    def post_link_submission(self, subverse, title, url):
        url = API_URL + 'v/{}'.format(subverse)
        body = json.dumps({'title':title,'url':url})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp['data']['id']

    def post_reply_to_submission(self, submission_id, comment):
        subverse = self.get_subverse_name(self.get_submission_by_id(submission_id))
        url = API_URL + 'v/{}/{}/comment'.format(subverse, submission_id)
        body = json.dumps({'Value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp['data']['id']

    def post_reply_to_comment(self, comment_id, comment):
        submission_id = self.get_comment_submission(self.comment_from_id(comment_id))
        subverse = self.get_subverse_name(self.get_submission_by_id(submission_id))
        url = API_URL + 'v/{}/{}/comment/{}'.format(subverse, submission_id, comment_id)
        body = json.dumps({'Value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp['data']['id']

    def post_reply_to_pm(self, pm_id, comment):
        url = API_URL + 'comments/{}'.format(pm_id)
        body = json.dumps({'Value':comment})
        r = requests.post(url, headers=self.headers, data=body)
        resp = json.loads(r.text)
        r.connection.close()
        return resp['data']['id']
    
    # SUBVERSE GETTER

    def get_subverse(self, subverse):
        submissions = self.get_submissions_by_subverse(subverse)
        return [(submission, self.get_comments_to_submission(self.get_id(sub))) for submission in submissions]



    # SUBMISSION GETTERS

    def get_submission_by_id(self, submission_id):
        url = API_URL + 'submissions/{}'.format(submission_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    def get_submissions_by_subverse(self, subverse):
        url = API_URL + 'v/{}'.format(subverse)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else []

    def get_content_submissions_by_subverse(self, subverse):
        return filter(self.is_content_submission, self.get_submissions_by_subverse(subverse))

    def get_url_submissions_by_subverse(self, subverse):
        return filter(self.is_url_submission, self.get_submissions_by_subverse(subverse))

    # COMMENT GETTERS

    def get_comment_by_id(self, comment_id):
        url = API_URL + 'comments/{}'.format(comment_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else {}

    def get_comments_to_submission(self, submission_id):
        subverse = self.get_subverse_name(self.get_submission_by_id(submission_id))
        url = API_URL + 'v/{}/{}/comments'.format(subverse, submission_id)
        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        r.connection.close()
        return resp['data'] if resp['success'] == True else []

    # VOAT DICT FUNCS
    
    @catch_empty_input
    def get_content(self, voat_dict, ignore_links=False):
        if (voat_dict != {}) and (ignore_links == True):
            return voat_dict['content']
        elif (voat != {}) and (ignore_links == False):
            if self.is_url_submission(voat_dict):
                return voat_dict['url']
            else:
                return voat_dict['content']
        else:
            return {}

    @catch_empty_input
    def get_subverse_name(self, voat_dict):
        if self.is_submission(voat_dict):        
            return voat_dict['subverse']
        else:
            submission_id = self.get_comment_submission(voat_dict)
            #return self.get_subverse(self.submission_from_id(submission_id))
            return self.get_submission_by_id(submission_id)['subverse']

    @catch_empty_input
    def get_author(self, voat_dict):
        return voat_dict['userName']

    @catch_empty_input
    def get_scores(self, voat_dict):
        return voat_dict['upVotes'], voat_dict['downVotes']

    @catch_empty_input
    def get_score(self, voat_dict):
        if voat_dict != {}:
            up, down = self.get_scores(voat_dict)
            return up - down
        else:
            return {}

    @catch_empty_input
    def get_date(self, voat_dict):
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

    @catch_empty_input
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



