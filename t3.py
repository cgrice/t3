import sys
from os import getcwd


class t3:

    def __init__(self):
        self.cwd = getcwd()
        print self.cwd
        #self.db = t3DB()
        #self.current_ticket = db.CurrentTicket()
        #self.status = db.Status()
    def main(self, args):
        for arg in args:
            # checkout - take ownership of a ticket, ready to punch in / punch out
            if arg == 'co' or arg == 'checkout':
                self.checkout(args[3])
                break
            # punch in - tell t3 that you are working on a specific ticket
            #            $ t3 pi will punch in to your last used ticket
            #            $ t3 pi 14 will punch in to ticket 14
            if arg == 'pi' or arg == 'punch-in':
                punchout()
                if(len(args) > 1):
                    self.checkout(args[1])
                    self.punchin(args[1])
                else:
                    self.punchin(current_ticket)
                break
            # punch out - stop working on your current ticket.
            if arg == 'po' or arg == 'punch-out':
                self.punchout()
                break

    def checkout(self, ticket):
        print 'Now working on ticket ' + ticket

    def punchin(self, ticket):
        print 'Punching in - ticket #' + ticket

    def punchout(self):
        print 'Punched out'

if __name__ == '__main__':
    t = t3()
    t.main(sys.argv[1:])

