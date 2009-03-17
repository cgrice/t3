import os

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
    print "\nInstalling T3"
    os.system("mkdir /usr/lib/t3")
    os.system("cp -r ./lib/*.py /usr/lib/t3/")
    os.system("chmod a+x /usr/lib/t3/t3.py")
    os.system("ln -s /usr/lib/t3/t3.py /usr/bin/t3")
    print "Installed OK"
    print "Configuration options are in ~/.t3/t3.conf"
    
