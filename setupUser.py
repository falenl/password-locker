#! python3
# setup.py - Used to setup password and key to access password locker.

import sys, getpass, shelve,os
from keytool import *
from user import *

if not os.path.exists('data'):
    os.makedirs('data')

username = getpass.getuser()
print('Username: %s' % username)
shelfFile = shelve.open('data/data')

keyword = ''
userExist = False

def askPassword():
    pwd = ' '
    repPwd = ''
    
    while pwd != repPwd:
        pwd = getpass.getpass('Please enter your new password:')
        while repPwd.strip() == '':
                repPwd = getpass.getpass('Please re-enter your new password:')

        if pwd != repPwd:
            print('The Passwords you entered did not matched')
            repPwd = ''

    return pwd

def enterPwd():
    global keyword, user
    passed = False
    if userExist:
        while not passed:
            pwd = getpass.getpass('Please enter your current password:')            
            keytool = Keytool(pwd)
            keytool.loadKeyFromFile('data/keyfile')           
            user = User(username, shelfFile, keytool)
            passed = user.matchPassword(pwd)
    keyword = askPassword()

if username in shelfFile:
    yesno = ''
    while yesno.lower() != 'n' and yesno.lower() != 'y':
        print('User "%s" has been setup. Do you want to change password?(y/n)')
        yesno = input()

    if yesno == 'n':
        sys.exit()
    else:
        userExist = True

enterPwd()

try:
    keytool = Keytool(keyword)
    keytool.loadKeyFromFile('data/keyfile')    
    if userExist:
        user.changePassword(keytool)
    shelfFile[username] = keytool.encrypt(keyword, True)
    shelfFile.close()
    print('Password has been saved successfully.')
except:
    print('Failed to save password')
