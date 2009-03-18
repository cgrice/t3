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
        self.cursor.execute('''CREATE TABLE tickets(ticket_number INTEGER PRIMARY KEY, estimate INTEGER, open INTEGER)''')
        self.conn.commit()
        
    def currentTicket(self):
        self.cursor.execute('''SELECT * FROM updates LIMIT 1 OFFSET (SELECT COUNT(update_id) FROM updates)-1''')
        result = self.cursor.fetchall()
        if(len(result) > 0):
            return { 'update_id':result[0][0],
                     'timestamp':result[0][1],
                     'ticket':result[0][2],
                     'punched_in':result[0][3],
                   }
        else:
            return {}

    def update(self, ticket, punch):
        self.cursor.execute('''INSERT INTO updates(timestamp, ticket_number, punched_in)
                               VALUES( ?, ?, ? )''', (time(), ticket, punch))
        self.topen(ticket)
        self.conn.commit()

    def close(self, ticket):
        self.cursor.execute('''UPDATE tickets SET open = 0 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()

    def topen(self, ticket):
        self.cursor.execute('''UPDATE tickets SET open = 1 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()

    def timeForTicket(self, ticket):
        self.cursor.execute("SELECT timestamp, punched_in FROM updates WHERE ticket_number = '" + str(ticket) + "'" )
        results = self.cursor.fetchall()
        ttime = 0
        if len(results) < 1:
            return 0
        timestamp = float(results[0][0])
        counting = False
        for result in results:
            if(result[1] != 1):
                if(counting):
                    ttime = ttime + (float(result[0]) - timestamp)
                timestamp = float(result[0])
                counting = False
            elif(result[1] == 1):
                timestamp = float(result[0])
                counting = True
        if results[-1][1] == 1:
            timenow = time();
            ttime = ttime + (timenow - timestamp)
        return ttime   

    def getTimeList(self):
        self.cursor.execute('''SELECT DISTINCT updates.ticket_number FROM updates JOIN tickets ON updates.ticket_number = tickets.ticket_number WHERE tickets.open != 0''')
        tickets = self.cursor.fetchall()
        tlist = []
        for ticket in tickets:
            tlist.append( (ticket[0], self.timeForTicket(ticket[0]), self.getEstimate(ticket[0])) )
        return tlist
    
    def getFullList(self):
        self.cursor.execute('''SELECT DISTINCT ticket_number FROM tickets 
WHERE tickets.open != 0''')
        tickets = self.cursor.fetchall()
        tlist = []
        for ticket in tickets:
            tlist.append( (ticket[0], self.timeForTicket(ticket[0]), self.getEstimate(ticket[0])) )
        return tlist

    def validTicket(self, ticket):
        self.cursor.execute('''SELECT DISTINCT COUNT(ticket_number) FROM updates WHERE ticket_number = ?''', (ticket,))
        results = self.cursor.fetchall()
        if(results[0][0] > 0):
            return True
        else:   
            return False

    def makeEstimate(self, ticket, estimate):
        if self.validTicket(ticket):
            self.cursor.execute('''UPDATE tickets SET estimate = ? WHERE ticket_number = ?''', (estimate, ticket))
            self.conn.commit()
        else:
            self.cursor.execute('''INSERT INTO tickets (ticket_number, estimate, open) VALUES (?, ?, ?)''', (ticket, estimate, '1'))
            self.conn.commit()

    def getEstimate(self, ticket):
        self.cursor.execute('''SELECT estimate FROM tickets WHERE ticket_number = ?''', (ticket,))
        r = self.cursor.fetchall()
        if len(r) < 1:
            return 1
        else:
            if r[0][0] == None:
                return 0
            else:
                return r[0][0]

    def clean(self):
        self.cursor.execute('''UPDATE tickets SET open = 0 WHERE 1''')
        self.conn.commit()
