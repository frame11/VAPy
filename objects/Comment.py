
class Comment:

    def __init__(self, comment_dict, subverse):
        
        self.comment_id = comment_dict['id']
        self.submission_id = comment_dict['submissionID']
        self.author = comment_dict['userName']
        self.subverse = subverse
        self.upvotes = comment_dict['upvotes']
        self.downvotes = comment_dict['downvotes']
        self.views = comment_dict['views']
        self.content = comment_dict['content']
        
        self.permalink = "https://fakevout.azurewebsites.net/v/{}/comments/{}/{}".format(
                          self.subverse, self.submission_id, self.comment_id)
