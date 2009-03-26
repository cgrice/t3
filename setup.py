import os

print 'Checking dependencies...'

can_install = True
success = False

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
    uid = os.geteuid()
    gid = os.getegid()
    home = os.path.expanduser('~')
    os.system("sudo mkdir /usr/lib/t3")
    os.system("sudo cp -r ./lib/*.py /usr/lib/t3/")
    os.system("sudo chmod a+x /usr/lib/t3/t3.py")
    os.system("sudo ln -s /usr/lib/t3/t3.py /usr/bin/t3")
    os.system(" mkdir ~/.t3")
    os.system("cp ./t3.conf ~/.t3/t3.conf")
    print "Installed OK"
    print "Configuration options are in ~/.t3/t3.conf"
    
