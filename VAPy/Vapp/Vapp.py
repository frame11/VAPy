import getpass

try:
    import ujson as json
except:
    import json

import VAPy

class Vapp(object):


    def __init__(self):
        
        self.load_config()
        self.vapy = VAPy.VAPy()
        pwd = getpass.getpass(prompt="Enter password: ")
        self.vapy.load_profile(self.profile, pwd)

        subverses = []
        self.nsfw = False


    def load_config(self):
        with open('./Vapp/config.json') as cf:
            config = json.load(cf)
        for key in config.keys():
            setattr(self, key, config[key])
