
import getpass, simplecrypt, sqlite3

from PersistenceService import PersistenceService

class Profiles(PersistenceService):

    def __init__(self):
        super(Profiles, self).__init__("profiles")

    # HELPERS

    def initialize_database(self):
        self.connect()
        self.c.execute("CREATE TABLE profiles (profile text, uname text, api_key text, token text)")
        self.db.commit()
        self.db.close()

    def add_profile(self, profile, uname, pwd, api_key):
        
        self.c.execute("SELECT COUNT(*) FROM profiles WHERE profile=?", (profile,))
        result = self.c.fetchone()
        if not result[0] == 0:
            print("Profile '{}' already exists in Profiles.")
        else :
            import VAPy
            vapy = VAPy.VAPy()
            token = vapy.get_token(uname, pwd, api_key)
            if not token:
                print("VAPy was unable to retreive a Voat API token with the credentials you provided.")
            else:
                print("Encrypting and storing Voat API credentials. This may take a moment.")
                ctoken = simplecrypt.encrypt(pwd, token)
                cuname = simplecrypt.encrypt(pwd, uname)
                capi_key = simplecrypt.encrypt(pwd, api_key)
                
                self.c.execute("INSERT INTO profiles (profile, uname, api_key, token) VALUES (?,?,?,?)"
                                , (profile, cuname, capi_key, ctoken))

                self.db.commit()

    def list_profiles(self):
        self.c.execute("SELECT profile FROM profiles")
        result = self.c.fetchall()
        profile_lst = [r[0] for r in result]
        print(*profile_lst, sep="\n")


    def get_profile(self, profile, pwd):
        self.c.execute("SELECT * FROM profiles WHERE profile=?", (profile,))
        res = self.c.fetchone()
        uname = simplecrypt.decrypt(pwd, res[1]).decode('utf-8')
        api_key = simplecrypt.decrypt(pwd, res[2]).decode('utf-8')
        token = simplecrypt.decrypt(pwd, res[3]).decode('utf-8')
        return (uname, pwd, api_key, token)

    def remove_profile(self, profile):
        self.c.execute("SELECT COUNT(*) FROM profiles WHERE profile=?", (profile,))
        result = self.c.fetchone()
        if result[0] == 0:
            print("The profile {} does not exist. Please recheck input.".format(profile))
        else:
            self.c.execute("DELETE FROM profiles WHERE profile=?", (profile,))
            self.db.commit()
            print("Profile {} has been removed.".format(profile))

                    
def standalone():
    print("::VAPy Profile Management::")
    
    p = Profiles()

    run = True

    while run:
    
        mode = input("Select 'a'dd, 'r'emove, 'l'ist, re'i'nitialize, 'q'uit: ")
    
        if mode == 'a':
            print("Creating new profile")
            profile = input("Enter profile name (Voat app name): ")
            uname = input("Enter Voat user name: ")
            pwd = getpass.getpass(prompt="Enter Voat password: ")
            pwd2 = getpass.getpass(prompt="Confirm Voat password: ")
            while pwd != pwd2:
                print("Passwords did not match.")
                pwd = getpass.getpass(prompt="Enter Voat password: ")
                pwd2 = getpass.getpass(prompt="Confirm Voat password: ")
            key = input("Enter Voat api key: ")
            p.add_profile(profile, uname, pwd, key)
            print("Api token successfully retreived.")
            print("Voat credentials encrypted and added to database.")

        elif mode == 'r':
            profile = input("Enter name of profile to remove from database: ")
            print("This action will delete {} from profiles.".format(profile))
            inp = input("This action cannot be undone. Confirm with 'Y': ")
            if inp == 'Y':
                p.remove_profile(profile)
            else:
                print("Action cancelled.")
        
        elif mode == 'i':
            print("This will erase all profiles from the database. This action cannot be undone. It is probably not what you actually want to do.")
        
        elif mode == 'l':
            p.list_profiles()
        
        elif mode == 'q':
            sys.exit()
        
        else:
            print("Invalid selection")

if __name__ == '__main__':
    standalone()
