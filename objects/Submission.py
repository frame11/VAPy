

class Submission:

    def __init__(self, submission_dict):
        
        self.s_id = submission_dict['id']
        self.author = submission_dict['userName']
        self.subverse = submission_dict['subverse']
        self.upvotes = submission_dict['upvotes']
        self.downvotes = submission_dict['downvotes']
        self.comment_count = submission_dict['commentCount']
        self.views = submission_dict['views']
        self.s_type = submission_dict['type']
        self.title = submission_dict['title']
        self.url = None
        self.content = None
        
        if self.s_type == 1:
            self.content = submission_dict['content']
        else:
            self.url = submission_dict['url']

        self.permalink = "https://fakevout.azurewebsites.net/v/{}/comments/{}".format(self.subverse, self.s_id)
