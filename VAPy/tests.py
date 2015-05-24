import getpass, unittest
import VAPy

class VAPyTests(unittest.TestCase):

    # SETUP

    @classmethod
    def setUpClass(VAPyTests):
        VAPyTests.pwd = getpass.getpass(prompt="Enter password for test profile: ")
        


    def setUp(self):
        self.vapy = VAPy.VAPy()
        self.vapy.load_profile("test", self.pwd)

    # HELPER TESTS

    def test_get_token(self):
        self.assertIn('Authorization', self.vapy.headers.keys())

    # SUBVERSE INFO TESTS
    def test_valid_get_subverse_creation_date(self):
        self.assertEqual(self.vapy.get_subverse_creation_date('api'), '2015-04-08T22:46:02.477')

    def test_invalid_get_subverse_creation_date(self):
        self.assertEqual(self.vapy.get_subverse_creation_date('yoloswagbotfactorystar'), {})
    
    def test_valid_get_subverse_subscriber_count(self):
        self.assertIsInstance(self.vapy.get_subverse_subscriber_count("api"), int)

    def test_invalid_get_subverse_subscriber_count(self):
        self.assertEqual(self.vapy.get_subverse_subscriber_count('yoloswagbotfactorystar'), {})

    def test_get_sfw_subverse_rated_adult(self):
        self.assertFalse(self.vapy.get_subverse_rated_adult('api'))

    def test_get_nsfw_subverse_rated_adult(self):
        self.assertTrue(self.vapy.get_subverse_rated_adult('frame11'))

    def test_invalid_get_subverse_rated_adult(self):
        self.assertEqual(self.vapy.get_subverse_rated_adult('yoloswapbotfactorystar'), {})

    def test_get_valid_subverse_sidebar(self): 
        self.assertEqual(self.vapy.get_subverse_sidebar('frame11'), '<h1>Home of VAPy</h1>\n')

    def test_invalid_get_subverse_sidebar(self):
        self.assertEqual(self.vapy.get_subverse_sidebar('yoloswagbotfactorystar'), {})

    # VOAT DICT FUNCTIONS
    
    def test_get_text_submission_content(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_submission_by_id(209)), 'testicular') 

    def test_get_text_submission_content_with_ignore_links(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_submission_by_id(209), ignore_links=True), 'testicular')
    
    def test_get_requested_url_submission_content(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_submission_by_id(211)), 'https://github.com/frame11/VAPy')

    def test_get_invalid_submission_content(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_get_comment_content(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_comment_by_id(2635)), 'attempt')

    def test_get_invalid_get_comment_content(self):
        self.assertEqual(self.vapy.get_content(self.vapy.get_comment_by_id(99999999)), {})

    def test_get_valid_submission_subverse(self):
        self.assertEqual(self.vapy.get_subverse(self.vapy.get_submission_by_id(209)), 'frame11')

    def test_get_invalid_submission_subverse(self):
        self.assertEqual(self.vapy.get_subverse(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_get_comment_subverse(self):
        self.assertEqual(self.vapy.get_subverse(self.vapy.get_comment_by_id(2635)), 'frame11')

    def test_get_invalid_get_comment_subverse(self):
        self.assertEqual(self.vapy.get_subverse(self.vapy.get_comment_by_id(99999999)), {})

    def test_get_valid_submission_author(self):
        self.assertEqual(self.vapy.get_author(self.vapy.get_submission_by_id(209)), 'frame11')
    
    def test_get_invalid_submission_author(self):
        self.assertEqual(self.vapy.get_author(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_get_comment_author(self):
        self.assertEqual(self.vapy.get_author(self.vapy.get_comment_by_id(2635)), 'frame11')
    
    def test_get_invalid_get_comment_author(self):
        self.assertEqual(self.vapy.get_author(self.vapy.get_comment_by_id(99999999)), {})
        
    def test_get_valid_submission_scores(self):
        self.assertEqual(self.vapy.get_scores(self.vapy.get_submission_by_id(213)), (3, 1))

    def test_get_invalid_submission_scores(self):
        self.assertEqual(self.vapy.get_scores(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_get_comment_scores(self):
        self.assertEqual(self.vapy.get_scores(self.vapy.get_comment_by_id(2635)), (1, 0))

    def test_get_invalid_get_comment_scores(self):
        self.assertEqual(self.vapy.get_scores(self.vapy.get_comment_by_id(99999999)), {})
        
    def test_get_valid_submission_score(self):
        self.assertEqual(self.vapy.get_score(self.vapy.get_submission_by_id(213)), 2)
    
    def test_get_invalid_submission_score(self):
        self.assertEqual(self.vapy.get_score(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_get_comment_score(self):
        self.assertEqual(self.vapy.get_score(self.vapy.get_comment_by_id(2635)), 1)

    def test_get_invalid_get_comment_score(self):
        self.assertEqual(self.vapy.get_score(self.vapy.get_comment_by_id(99999999)), {})

    def test_get_valid_submission_date(self):
        self.assertEqual(self.vapy.get_date(self.vapy.get_submission_by_id(209)), '2015-05-07T08:41:44.067')

    def test_get_invalid_submission_date(self):
        self.assertEqual(self.vapy.get_date(self.vapy.get_submission_by_id(99999999)), {})
    
    def test_get_valid_get_comment_date(self):
        self.assertEqual(self.vapy.get_date(self.vapy.get_comment_by_id(2635)), '2015-05-08T19:17:51.9')

    def test_get_invalid_get_comment_date(self):
        self.assertEqual(self.vapy.get_date(self.vapy.get_comment_by_id(99999999)), {})

    # SUBMISSION DICT FUNCTIONS

    def test_get_text_submission_type(self):
        self.assertEqual(self.vapy.get_submission_type(self.vapy.get_submission_by_id(209)), 'content')
        
    def test_get_link_submission_type(self):
        self.assertEqual(self.vapy.get_submission_type(self.vapy.get_submission_by_id(211)), 'url')
        
    def test_get_invalid_submission_type(self):
        self.assertEqual(self.vapy.get_submission_type(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_submission_title(self):
        self.assertEqual(self.vapy.get_submission_title(self.vapy.get_submission_by_id(209)), 'testicular')
        
    def test_get_invalid_submission_title(self):
        self.assertEqual(self.vapy.get_submission_title(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_submission_rank(self):
        self.assertEqual(self.vapy.get_submission_rank(self.vapy.get_submission_by_id(213)), 0.172865)

    def test_get_invalid_submission_rank(self):
        self.assertEqual(self.vapy.get_submission_rank(self.vapy.get_submission_by_id(99999999)), {})

    def test_get_valid_submission_get_comment_count(self):
        self.assertEqual(self.vapy.get_submission_comment_count(self.vapy.get_submission_by_id(213)), 3)

    def test_get_invalid_submission_get_comment_count(self):
        self.assertEqual(self.vapy.get_submission_comment_count(self.vapy.get_submission_by_id(99999999)), {})


    # FILTER TESTS

    def test_pos_valid_submission_contains_regex_in_title(self):
        self.assertTrue(self.vapy.contains_regex_in_title('test', self.vapy.get_submission_by_id(209)))

    def test_neg_valid_submission_contains_regex_in_title(self):
        self.assertFalse(self.vapy.contains_regex_in_title('pasta', self.vapy.get_submission_by_id(209)))

    def test_invalid_submission_contains_regex_in_title(self):
        self.assertFalse(self.vapy.contains_regex_in_title('pasta', self.vapy.get_submission_by_id(99999999)))

    def test_pos_valid_text_submission_contains_regex_in_content(self):
        self.assertTrue(self.vapy.contains_regex_in_content('test', self.vapy.get_submission_by_id(213)))

    def test_neg_valid_text_submission_contains_regex_in_content(self):
        self.assertFalse(self.vapy.contains_regex_in_content('pasta', self.vapy.get_submission_by_id(213)))

    def test_pos_valid_link_submission_contains_regex_in_content(self):
        self.assertTrue(self.vapy.contains_regex_in_content('test', self.vapy.get_submission_by_id(213)))

    def test_neg_valid_link_submission_contains_regex_in_content(self):
        self.assertFalse(self.vapy.contains_regex_in_content('pasta', self.vapy.get_submission_by_id(213)))
    
    def test_pos_valid_link_submission_contains_regex_in_link(self):
        self.assertTrue(self.vapy.contains_regex_in_link('github', self.vapy.get_submission_by_id(211)))
    
    def test_neg_valid_link_submission_contains_regex_in_link(self):
        self.assertFalse(self.vapy.contains_regex_in_link('pasta', self.vapy.get_submission_by_id(211)))

    def test_valid_text_submission_contains_regex_in_link(self):
        self.assertFalse(self.vapy.contains_regex_in_link('pasta', self.vapy.get_submission_by_id(209)))

    def test_invalid_submission_contains_regex_in_link(self):
        self.assertFalse(self.vapy.contains_regex_in_link('github', self.vapy.get_submission_by_id(99999999)))

    def test_pos_in_title_valid_submission_contains_regex(self):
        self.assertTrue(self.vapy.contains_regex('test', self.vapy.get_submission_by_id(209)))

    def test_pos_in_text_content_valid_submission_contains_regex(self):
        self.assertTrue(self.vapy.contains_regex('test', self.vapy.get_submission_by_id(213)))

    def test_pos_in_link_content_valid_submission_contains_regex(self):
        self.assertTrue(self.vapy.contains_regex('github', self.vapy.get_submission_by_id(211)))

    def test_pos_in_both_valid_submission_contains_regex(self):
        self.assertTrue(self.vapy.contains_regex('not', self.vapy.get_submission_by_id(213)))

    def test_neg_valid_submission_contains_regex(self):
        self.assertFalse(self.vapy.contains_regex('pasta', self.vapy.get_submission_by_id(213)))
    
    def test_invalid_submission_contains_regex(self):
        self.assertFalse(self.vapy.contains_regex('pasta', self.vapy.get_submission_by_id(99999999)))

    def test_pos_valid_get_comment_contains_regex(self):
        self.assertTrue(self.vapy.contains_regex('spin', self.vapy.get_comment_by_id(2609)))

    def test_neg_valid_get_comment_contains_regex(self):
        self.assertFalse(self.vapy.contains_regex('pasta', self.vapy.get_comment_by_id(2609)))

    def test_invalid_get_comment_contains_regex(self):
        self.assertFalse(self.vapy.contains_regex('pasta', self.vapy.get_comment_by_id(99999999)))



if __name__ == '__main__':
    unittest.main()
