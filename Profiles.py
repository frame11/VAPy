
import getpass, os, platform, simplecrypt, sqlite3

class Profiles:

    def __init__(self):
        
        #Set working directory for data persistence
        sys = platform.system()
        if sys == 'linux':
            self.wd = '/var/lib/vapy/'
        elif sys == 'win32' or 'win64':
            pass
        elif sys == 'darwin':
            pass


    def check_for_initial_run(self):
        if not os.path.isdir(self.wd):
            os.makedirs(self.wd)
            self.db = sqlite3.connect(self.wd + "profiles")
            self.c = self.db.cursor()
            self.c.execute("CREATE TABLE profiles (agent_name text, uname text, pwd text, api_key text, token text)")
            self.db.commit()
            self.db.close()

    def add_profile(self, agent_name, uname, pwd, api_key):
        
        self.c.execute("SELECT COUNT(*) FROM profiles WHERE agent_name=?", (agent_name,))
        result = self.c.fetchone()
        if not result[0] == 0:
            print("Agent '{}' already exists in Profiles.")
        else :
            import VAPy
            token = VAPy.VAPy.get_token(api_key, uname, pwd)
            ctoken = simplecrypt.encrypt(token, pwd)
            cuser = simplecrypt.encrypt(user, pwd)
            cpwd = simplecrypt.encrypt(pwd, pwd)
            capi_key = simplecrypt(api_key, pwd)


    def get_list_of_profiles(self):
        pass
