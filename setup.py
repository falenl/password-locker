#! python3
# setup.py - Used to setup password and key to access password locker.

import sys, getpass, shelve
from keytool import *

if len(sys.argv) < 2:
    print('Usage: python setup.py [username]')
    sys.exit()

username = sys.argv[1]

keyword = ''
while keyword.strip() == '':  
    keyword = getpass.getpass('Please enter your password:')

keytool = Keytool(keyword)
shelfFile = shelve.open('data')
keytool.loadKeyFromFile('keyfile')
keytool.loadKey()

#try:
shelfFile[username] = keytool.encrypt(keyword, True)
print(shelfFile[username])
shelfFile.close()
print('Password has been saved successfully.')
#except:
    #print('Failed to save password')
