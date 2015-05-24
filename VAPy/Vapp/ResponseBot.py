import Vapp

class ResponseBot(Vapp):

    def __init__(self, profile=""):
        super(ResponseBot, self).__init__(profile=profile)


    def run(self):

        content = [self.get_content(subverse, self.target_content) for subverse in self.subverses]




