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
        self.assertIn('Authorization', self.vapy.headers)

    def test_get_subverse_creation_date(self):
        self.assertEqual(self.vapy.get_subverse_creation_date('api'), '2015-04-08T22:46:02.477')

    def test_get_subverse_subscriber_count(self):
        self.assertIsInstance(self.vapy.get_subverse_subscriber_count("api"), int)

    def test_get_subverse_rated_adults(self):
        self.assertFalse(self.vapy.get_subverse_rated_adult('api'))

if __name__ == '__main__':
    unittest.main()
