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
        self.cursor.execute('''CREATE TABLE tickets(ticket_number INTEGER PRIMARY KEY, estimate INTEGER, open INTEGER, complete INTEGER)''')
        self.conn.commit()
        self.clean()
        
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

    def complete(self, ticket):
        self.cursor.execute('''UPDATE tickets SET complete = 1 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()

    def uncomplete(self, ticket):
        self.cursor.execute('''UPDATE tickets SET complete = 0 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()


    def close(self, ticket):
        self.cursor.execute('''UPDATE tickets SET open = 0 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()

    def topen(self, ticket):
        self.cursor.execute('''UPDATE tickets SET open = 1 WHERE ticket_number = ?''', (ticket,))
        self.conn.commit()

    def timeForTicket(self, ticket):
        self.cursor.execute('''SELECT MAX(update_id) FROM updates WHERE ticket_number = \'-1\'''')
        results = self.cursor.fetchall()
        cutoff = results[0][0]
        self.cursor.execute("SELECT timestamp, punched_in FROM updates WHERE ticket_number = '" + str(ticket) + "' AND update_id > ?", (cutoff,) )
        results = self.cursor.fetchall()
        return self.timeForRange(results)
      
    def timeForRange(self, results):
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

    def getIterations(self, ticket):
        iterations = []
        self.cursor.execute('''SELECT update_id, timestamp FROM updates WHERE ticket_number = \'-1\'''')
        cleans = self.cursor.fetchall()
        index = 0
        for clean in cleans:
            query = "SELECT timestamp, punched_in FROM updates WHERE ticket_number = ? AND update_id > ? "
            try:  
                starts = cleans[index][0]
                ends = cleans[index+1][0]  
                query += "AND update_id < ?"
                itend = cleans[index+1][1]
                self.cursor.execute(query, (ticket, starts, ends) )
            except: 
                break
            results = self.cursor.fetchall()
            iterations.append([itend, (ticket, self.timeForRange(results))])
            index += 1
        return iterations

    def getAllTickets(self):
        self.cursor.execute('''SELECT DISTINCT ticket_number FROM updates WHERE ticket_number != \'-1\'''')
        tlist = self.cursor.fetchall()
        return tlist

    def getLogsForTicket(self, ticket):
        self.cursor.execute('''SELECT timestamp, punched_in FROM updates WHERE ticket_number = ?''', (ticket,))
        results = self.cursor.fetchall()
        logs = []
        for result in results:
            log = {}
            log['status'] = result[1]
            log['timestamp'] = result[0]
            logs.append(log)
        return logs

    def getTimeList(self):
        self.cursor.execute('''SELECT MAX(update_id) FROM updates WHERE ticket_number = \'-1\'''')
        results = self.cursor.fetchall()
        cutoff = results[0][0]
        self.cursor.execute('''SELECT DISTINCT ticket_number FROM updates WHERE updates.update_id > ?''', (cutoff,))
        tickets = self.cursor.fetchall()
        tlist = []
        for ticket in tickets:
            tlist.append( (ticket[0], self.timeForTicket(ticket[0]), self.getEstimate(ticket[0])) )
        return tlist
    
    def getFullList(self):
        self.cursor.execute('''SELECT MAX(update_id) FROM updates WHERE ticket_number = \'-1\'''')
        results = self.cursor.fetchall()
        cutoff = results[0][0]
        self.cursor.execute('''SELECT DISTINCT updates.ticket_number, complete FROM updates LEFT JOIN tickets ON updates.ticket_number = tickets.ticket_number WHERE updates.update_id > ?''', (cutoff,))
        tickets = self.cursor.fetchall()
        tlist = []
        for ticket in tickets:
            tlist.append( (ticket[0], self.timeForTicket(ticket[0]), self.getEstimate(ticket[0]), ticket[1]) )
        return tlist

    def validTicket(self, ticket):
        self.cursor.execute('''SELECT DISTINCT COUNT(ticket_number) FROM
tickets WHERE ticket_number = ?''', (ticket,))
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
        self.cursor.execute('''INSERT INTO updates(timestamp, ticket_number, punched_in)
                               VALUES( ?, ?, ? )''', (time(), '-1', '-1'))
        self.conn.commit()
