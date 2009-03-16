from pysqlite2 import dbapi2 as sqlite

class t3DB:

    def __init__(self, path):
        if(is_file(path)):
            sqllite3_conn = sqlite.connect(path)
        else:
            sqllite3_conn = sqlite.connect(path)
            self._setupDB()
        self.cursor = sqllite3_conn.cursor()

    def _setupDB(self):
        # Set up tables
        c.execute('''CREATE TABLE updates(update_id INTEGER PRIMARY KEY, timestamp INTEGER NOT NULL, 
                     ticket_number NOT NULL, punched_in BOOLEAN NOT NULL)''')


