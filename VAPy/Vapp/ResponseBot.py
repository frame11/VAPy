import Vapp

class ResponseBot(Vapp):

    def __init__(self, profile=""):
        super(ResponseBot, self).__init__(profile=profile)


    def run(self):

        for subverse in self.target_subverses:
            
            submissions = self.vapy.submissions_from_subverse(subverse)



