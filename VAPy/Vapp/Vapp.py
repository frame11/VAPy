import getpass

try:
    import ujson as json
except:
    import json

import VAPy.VAPy

class Vapp(Object):

    def __init__(self, profile=""):
        self.vapy = VAPy.VAPy()
        pwd = getpass.getpass(prompt="Enter password: ")
        self.vapy.load_profile(profile, pwd)

        subverses = []
        self.nsfw = False


    def load_config(self):
        with open("./config.json") as cf:
            config = ujson.loads(cf.read())

        print(config)
