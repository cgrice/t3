from pysqlite2 import dbapi2 as sqlite
import os
from time import time
import datetime

class t3DB:

    def __init__(self, path):
        if(os.path.exists(path)):
            self.conn = sqlite.connect(path)
            self.cursor = self.conn.cursor()
        else:
            self.conn = sqlite.connect(path)
            self.cursor = self.conn.cursor()
            self._setupDB()

    def _setupDB(self):
        self.cursor.execute('''CREATE TABLE updates(update_id INTEGER PRIMARY KEY, timestamp VARCHAR(64) NOT NULL, 
                     ticket_number NOT NULL, punched_in BOOLEAN NOT NULL)''')
        self.conn.commit()
        
    def currentTicket(self):
        self.cursor.execute('''SELECT * FROM updates LIMIT 1 OFFSET (SELECT COUNT(update_id) FROM updates)-1''')
        result = self.cursor.fetchall()
        return { 'update_id':result[0][0],
                 'timestamp':result[0][1],
                 'ticket':result[0][2],
                 'punched_in':result[0][3]
               }

    def update(self, ticket, punch):
        self.cursor.execute('''INSERT INTO updates(timestamp, ticket_number, punched_in)
                               VALUES( ?, ?, ? )''', (time(), ticket, punch))
        self.conn.commit()

    def timeForTicket(self, ticket):
        self.cursor.execute('''SELECT timestamp, punched_in FROM updates WHERE ticket_number = ?''', (ticket,))
        results = self.cursor.fetchall()
        time = 0
        timestamp = float(results[0][0])
        counting = False
        for result in results:
            if(result[1]):
                counting = True
            else:
                counting = False
            if(counting):
                time = time + (float(result[0]) - timestamp)
                timestamp = float(result[0])
        return time        
