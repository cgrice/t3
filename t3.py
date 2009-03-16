#!/usr/bin/python

import sys
from os import getcwd
from db import t3DB


class t3:

    def __init__(self):
        self.cwd = getcwd()
        self.db = t3DB('./t3.db')
        self.current_ticket = self.db.currentTicket()
        #self.status = db.Status()
    def main(self, args):
        for arg in args:
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

    def checkout(self, ticket):
        if(self.current_ticket):
            if(self.current_ticket['ticket'] != ticket):
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
        print "Ticket\tTime Spent\t"
        for tl in tlist:
            if self.current_ticket['punched_in'] and self.current_ticket['ticket'] == tl[0]:
                current = "<--\t"
            else:
                current = "\t"
            print str(tl[0]) + "\t" + str(tl[1]) + current
            

if __name__ == '__main__':
    t = t3()
    t.main(sys.argv[1:])

