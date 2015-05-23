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

