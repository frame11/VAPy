import getpass, unittest
import VAPy

class VAPyTests(unittest.TestCase):
    
    def setUpClass(self):
        self.key = input("Please enter api_key: ")
        self.uname = input("Please enter username: ")
        self.pwd = getpass.getpass("Please enter password: ")
        
        
    def setUp(self):
        self.vapy = VAPy.VAPy(self.key, self.uname, self.pwd)


    def test_get_token(self):
        self.assertIn('Authorization', self.vapy.headers)


    def test_get_subverse_subscriber_count(self):
        self.assertIsInstance(self.vapy.get_subverse_subscriber_count("api"), int)

if __name__ == '__main__':
    unittest.main()
