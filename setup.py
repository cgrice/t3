print 'Checking dependencies...'

can_install = True

try:
    import pysqlite2
    print "python-pysqlite2\t OK"
except:
    print "python-pysqlite2\t NOT OK"
    print """T3 requires python-pysqlite2 to be installed. Please install this module."""
    can_install = False

try:
    import yaml
    print "python-yaml\t\t OK"
except: 
    print "python-yaml\t NOT OK"
    print """T3 requires python-yaml to be installed. Please install this module."""
    can_install = False

if can_install:
    print "\nCopying t3 src to /usr/lib/t3/"
    

