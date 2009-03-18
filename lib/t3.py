#!/usr/bin/python

import sys
import os
from db import t3DB
import yaml
from time import time

class t3:

    def __init__(self):
        self.version = '0.1'
        self.cwd = os.getcwd()
        self.db = t3DB(os.path.expanduser('~') + '/.t3/t3.db')
        self.current_ticket = self.db.currentTicket()
        self.conf = yaml.load(open(os.path.expanduser('~') + '/.t3/t3.conf'))
        #self.status = db.Status()
    def main(self, args):
        for arg in args:    
            if arg == 'status':
                print ' Ticket Time Tracker v'+self.version
                print "-----------------------------------------------"
                if self.punchedIn():
                    print '  Punched into ticket #' + self.current_ticket['ticket'] + ' for ' + self.lastDiff(self.current_ticket["ticket"])
                else: 
                    print '  Punched out'
                print '-----------------------------------------------'
                print " Ticket status"
                print "-----------------------------------------------"
                self.getList()
            elif arg == 'init':
                self.db = t3DB('./' + args[1] + '.db')
                print 'Created t3 store in ' + os.getcwd()
            elif arg == 'pi' or arg == 'punch-in':
                if(len(args) > 1):
                    self.punchin(args[1])
                else:
                    self.punchin(self.current_ticket["ticket"])
            elif arg == 'po' or arg == 'punch-out':
                self.punchout()
            elif arg == 'time':
                self.getTime(args[1])
            elif arg == 'list' or arg == 'ls':
                self.getList()
            elif arg == 'close':
                self.close(args[1])
            elif arg == 'open':
                self.topen(args[1])
            elif arg == 'estimate' or arg == 'est':
                ticket = args[1]
                estimate = args[2]
                self.db.makeEstimate(ticket, estimate)
            elif arg == 'report':
                self.report()
            elif arg == 'purge' or arg == 'clean':
                self.db.clean()
            else:
                self.help()
                break
            
    def help(self):
        print "usage: t3 COMMAND [ARGS]"
        print '''\nThe most commonly used commands are:
    pi [ticket]             - punch in to a ticket and start tracking time
    po                      - punch out of any current tickets
    est [ticket] [estimate] - estimate the amount of points needed for a ticket
    close [ticket]          - mark a ticket as finished
    open [ticket]           - re-open a closed ticket
    purge                   - close all open tickets
    list | ls               - show currently open tickets
    status                  - show current ticket status and time spent
    report                  - generate statistics for all open tickets'''
    

    def punchedIn(self):
        if self.current_ticket and self.current_ticket['punched_in'] == 1:
            return True
        else:
            return False

    def close(self, ticket):
        self.punchout()
        self.db.close(ticket)
        print 'Closed ticket #' + ticket + ' - this ticket will not appear on any summaries'        

    def topen(self, ticket):
        self.db.topen(ticket)
        print 'Ticket #' + ticket + ' opened'

    def punchin(self, ticket):
        self.punchout()
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
        return time

    def getList(self):
        tlist = self.db.getTimeList()
        if len(tlist) < 1:
            print " No data - awaiting punch in"
        else:
            print " Ticket\tTime Spent\tPoints\tEstimated"
            for tl in tlist:
                if self.current_ticket['punched_in'] and self.current_ticket['ticket'] == tl[0]:
                    current = "\t<--\t"
                else:
                    current = "\t\t"
                time = self.formatTime(tl[1])
                points = self.makePoints(tl[1])
                estimated = str(self.db.getEstimate(tl[0]))
                print " " + str(tl[0]) + "\t" + time + "\t\t" + str(points) + "\t" + estimated + "\t" + current

    def formatTime(self, time):
        minutes = 0
        hours = 0
        seconds = int(time)
        if seconds > 60:
            minutes = int(time/60)
            seconds = int(round(time - (minutes * 60), 0))
        if minutes > 60:
            hours = int(minutes/60)
            minutes = minutes - (hours * 60)
        return (str(hours) + ':' + str(minutes) + ':' + str(seconds))

    def lastDiff(self, ticket):
        dtime = time() - float(self.current_ticket['timestamp'])
        return self.formatTime(dtime)

    def makePoints(self, time):
        unit = self.conf['point_unit']
        hours = time / 60 / 60
        pointsdone = hours / unit   
        return round(pointsdone, 1)

    def report(self):
        tlist = self.db.getFullList()
        totalpoints = 0
        totalestimate = 0
        diff = 0
        diffs = []
        for t in tlist:
            totalpoints += self.makePoints(t[1])   
            totalestimate += t[2]
            diffs.append(t[2] - self.makePoints(t[1]))
        if len(tlist) < 1:
            print ' No data available'
            return False
        print ' Report'
        print '-----------------------------------------------'
        print "  Total points estimated: \t" + str(totalestimate)
        print "  Total points done: \t\t" + str(totalpoints)
        print "  Total Difference: \t\t" + str(sum(diffs))
        print "  Average difference: \t\t" + str(sum(diffs) / len(diffs))
        print '-----------------------------------------------'
        print ' Breakdown'
        print '-----------------------------------------------'
        print " Ticket\tPoints\tEstimated\tDiff"
        for t in tlist:
            points = self.makePoints(t[1])
            diff = t[2] - self.makePoints(t[1])
            print " " + str(t[0]) + "\t" + str(points) + "\t" + str(t[2]) + "\t\t" + str(diff)

if __name__ == '__main__':
    t = t3()
    t.main(sys.argv[1:])

