import getpass, unittest
import VAPy

class VAPyTests(unittest.TestCase):
   
    @classmethod
    def setUpClass(VAPyTests):
        VAPyTests.key = input("Please enter api_key: ")
        VAPyTests.uname = input("Please enter username: ")
        VAPyTests.pwd = getpass.getpass("Please enter password: ")
        
        
    def setUp(self):
        self.vapy = VAPy.VAPy(self.key, self.uname, self.pwd)

    def test_get_token(self):
        self.assertIn('Authorization', self.vapy.headers.keys())

    def test_valid_get_subverse_creation_date(self):
        self.assertEqual(self.vapy.get_subverse_creation_date('api'), '2015-04-08T22:46:02.477')

    def test_invalid_get_subverse_creation_date(self):
        self.assertFalse(self.vapy.get_subverse_creation_date('yoloswagbotfactorystar'))
    
    def test_valid_get_subverse_subscriber_count(self):
        self.assertIsInstance(self.vapy.get_subverse_subscriber_count("api"), int)

    def test_invalid_get_subverse_subscriber_count(self):
        self.assertFalse(self.vapy.get_subverse_subscriber_count('yoloswagbotfactorystar'))

    def test_get_sfw_subverse_rated_adult(self):
        self.assertEqual(self.vapy.get_subverse_rated_adult('api'), 'unrated')

    def test_get_nsfw_subverse_rated_adult(self):
        self.assertEqual(self.vapy.get_subverse_rated_adult('frame11'), 'rated')

    def test_invalid_get_subverse_rated_adult(self):
        self.assertFalse(self.vapy.get_subverse_rated_adult('yoloswapbotfactorystar'))

    def test_get_valid_subverse_sidebar(self): 
        self.assertEqual(self.vapy.get_subverse_sidebar('frame11'), '<h1>Home of VAPy</h1>\n')

    def test_invalid_get_subverse_sidebar(self):
        self.assertFalse(self.vapy.get_subverse_sidebar('yoloswagbotfactorystar'))

    def test_get_text_submission_type(self):
        self.assertEqual(self.vapy.get_submission_type(self.vapy.submission_dict_from_id(209)), 'text')
        
    def test_get_link_submission_type(self):
        self.assertEqual(self.vapy.get_submission_type(self.vapy.submission_dict_from_id(211)), 'link')
        
    def test_get_invalid_submission_type(self):
        self.assertFalse(self.vapy.get_submission_type(self.vapy.submission_dict_from_id(99999999)))

    def test_get_test_submission_content(self):
        self.assertEqual(self.vapy.get_submission_content(self.vapy.submission_dict_from_id(209)), '<p>testicular</p>\n') 

if __name__ == '__main__':
    unittest.main()
