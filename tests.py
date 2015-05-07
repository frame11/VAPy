import getpass, unittest
import VAPy

class VAPyTests(unittest.TestCase):
    
    def setUp(self):
        self.key = input("Please enter api_key: ")
        self.uname = input("Please enter username: ")
        self.pwd = getpass.getpass("Please enter password: ")
        self.vapy = VAPy.VAPy(self.key, self.uname, self.pwd)


    def test_get_token(self):
        self.assertIn('Authorization', self.vapy.headers)


if __name__ == '__main__':
    unittest.main()
