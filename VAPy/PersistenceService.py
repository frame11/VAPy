import os, sqlite3, sys

class PersistenceService(object):

    def __init__(self, db_name):
        
        self.db_name = db_name

        #Set working directory for data persistence
        if sys.platform == 'linux':
            self.wd = os.path.expanduser('~') + "/.vapy/"
        elif sys == 'win32' or 'win64':
            pass
        elif sys == 'darwin':
            pass
        self.check_for_initial_run()
        self.connect()

    # HELPERS
    def connect(self):
        self.db = sqlite3.connect(self.wd + self.db_name)
        self.c = self.db.cursor()

    def check_for_initial_run(self):
        if not os.path.isdir(self.wd):
            os.makedirs(self.wd)
        if not os.path.isfile(self.wd + self.db_name):
            self.initialize_database()

    def initialize_database(self):
        return None
