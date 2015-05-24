import getpass

try:
    import ujson as json
except:
    import json

import VAPy

class Vapp(object):
    

    def __init__(self):

        self.app_name = ""        
        self.app_dir = "./"
        self.nsfw = False
        self.subverses = []

        self.getter_lookups = {
            "text submission titles": self.get_text_submission_titles,
            "link submission titles": self.get_link_submission_titles,
            "text submission content": self.get_text_submission_content,
            "link submission content": self.get_link_submission_content,
            "comments to text submissions": self.get_comments_to_text_submissions,
            "comments to link submissions": self.get_comments_to_link_submissions,
            "comments": self.get_comments,
            "titles": self.get_titles,
            "text": self.get_text,
            "all": self.get_all
        }
        
        self.load_config()
        if not self.validate_config_load():
            print("There is a problem with config.json")
            return None

        self.vapy = VAPy.VAPy()
        pwd = getpass.getpass(prompt="Enter password: ")
        self.vapy.load_profile(self.profile, pwd)
        



    def load_config(self):
        with open('./Vapp/config.json') as cf:
            config = json.load(cf)
        for key in config.keys():
            setattr(self, key, config[key])

    def validate_config_load(self):
        return True if (
                       type(self.app_name) == str and len(self.app_name) > 0 and
                       len(self.subverses) > 0
                       ) else False


    # Content getters

    def get_text_submission_titles(self, subverse):
        text_submissions = filter(self.vapy.is_content_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [self.vapy.get_title(sub_dict) for sub_dict in text_submissions]

    def get_link_submission_titles(self, subverse):
        link_submissions = filter(self.vapy.is_link_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [self.vapy.get_title(sub_dict) for sub_dict in link_submissions)]

    def get_text_submission_content(self, subverse):
        text_submissions = filter(self.vapy.is_content_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [self.vapy.get_content(sub_dict) for sub_dict in text_submissions] 
    
    def get_link_submission_content(self, subverse):
        link_submissions = filter(self.vapy.is_link_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [self.vapy.get_content(sub_dict) for sub_dict in link_submissions]

    def get_comments_to_text_submissions(self, subverse):
        text_submissions = filter(self.vapy.is_content_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [com_dict for com_dict in self.vapy.comment_dicts_from_submission(sub) for sub in text_submissions] 

    def get_comments_to_link_submissions(self, subverse):
        link_submissions = filter(self.vapy.is_link_submissions, self.vapy.submission_dicts_from_subverse(subverse))
        return [com_dict for com_dict in self.vapy.comment_dicts_from_submission(sub) for sub in link_submissions] 

    def get_comments(self, subverse):
        return self.get_comments_to_text_submissions(subverse) + self.get_comments_to_link_submissions(subverse)

    def get_titles(self, subverse):
        return self.get_text_submission_titles(subverse) + self.get_link_submission_titles(subverse)

    def get_text(self, subverse):
        return self.get_comments(subverse) + self.get_titles(subverse) + self.get_text_submission_content(subverse)

    def get_all(self, subverse):
        return self.get_text(subverse) + self.get_link_submission_content(subverse)

    def get_content(self, subverse, c_types):
        return [get_attr(self, getter_lookups[c_type])(subverse) for c_type in c_types]
        
