#!/usr/bin/python

import sys
import os
from db import t3DB
import yaml

class t3:

    def __init__(self):
        self.cwd = os.getcwd()
        self.db = t3DB(os.path.expanduser('~') + '/.t3/t3.db')
        self.current_ticket = self.db.currentTicket()
        self.conf = yaml.load(open(os.path.expanduser('~') + '/.t3/t3.conf'))
        #self.status = db.Status()
    def main(self, args):
        for arg in args:
            if arg == 'init':
                self.db = t3DB('./' + args[1] + '.db')
                print 'Created t3 store in ' + os.getcwd()
                break
            # checkout - take ownership of a ticket, ready to punch in / punch out
            if arg == 'co' or arg == 'checkout':
                self.checkout(args[1])
                break
            # punch in - tell t3 that you are working on a specific ticket
            #            $ t3 pi will punch in to your last used ticket
            #            $ t3 pi 14 will punch in to ticket 14
            if arg == 'pi' or arg == 'punch-in':
                if(len(args) > 1):
                    self.checkout(args[1])
                    self.punchin(args[1])
                else:
                    self.punchin(self.current_ticket)
                break
            # punch out - stop working on your current ticket.
            if arg == 'po' or arg == 'punch-out':
                self.punchout()
                break
            if arg == 'time':
                self.getTime(args[1])
                break
            if arg == 'list' or arg == 'ls':
                self.getList()
                break
            if arg == 'close':
                self.close(args[1])
                break

    def punchedIn(self):
        if self.current_ticket['punched_in'] == 1:
            return True
        else:
            return False

    def close(self, ticket):
        self.punchout()
        self.db.close(ticket)
        print 'Closed ticket #' + ticket + ' - this ticket will not appear on any summaries'        

    def checkout(self, ticket):
        if self.current_ticket and self.current_ticket['ticket'] != ticket and self.punchedIn():
            self.punchout()
        self.current_ticket['ticket'] = ticket
        print 'Now working on ticket ' + ticket

    def punchin(self, ticket):
        self.db.update(ticket, 1)
        print 'Punching in - ticket #' + ticket

    def punchout(self):
        if(self.current_ticket and self.current_ticket['punched_in'] == 1):
            self.db.update(self.current_ticket['ticket'], 0)
            print 'Punched out of ticket #' + self.current_ticket['ticket']
        else:
            print 'Not punched in to any tickets'

    def getTime(self, ticket):
        time =  self.db.timeForTicket(ticket)
        print time

    def getList(self):
        tlist = self.db.getTimeList()
        print "Ticket\tTime Spent\tPoints"
        for tl in tlist:
            if self.current_ticket['punched_in'] and self.current_ticket['ticket'] == tl[0]:
                current = "<--\t"
            else:
                current = "\t"
            time = self.formatTime(tl[1])
            points = self.makePoints(tl[1])
            print str(tl[0]) + "\t" + time + "\t\t" + str(points) + "\t" + current

    def formatTime(self, time):
        minutes = 0
        hours = 0
        seconds = time
        if seconds > 60:
            minutes = int(time/60)
            seconds = int(round(time - (minutes * 60), 0))
        if minutes > 60:
            hours = int(minutes/60)
            minutes = minutes - (hours * 60)
        return (str(hours) + ':' + str(minutes) + ':' + str(seconds))



    def makePoints(self, time):
        unit = self.conf['point_unit']
        hours = time / 60 / 60
        pointsdone = hours / unit   
        return round(pointsdone, 1)

if __name__ == '__main__':
    t = t3()
    t.main(sys.argv[1:])

