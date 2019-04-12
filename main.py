#!python

import sys, getpass, shelve, pyperclip
from keytool import *

user = getpass.getuser()
pwd = getpass.getpass("User Name : %s\nPassword:" % user)

keytool = Keytool()
shelfFile = shelve.open('data')

keytool.loadKey(pwd)
keytool.loadKeyFromFile('keyfile')

def printMenu():
    print('Menu'.center(30, "="))
    print('1. Enter/Update keyword')
    print('2. Search keyword')
    print('3. Exit')
    print(''.center(30, "="))
    print('Choose menu: ', end='')

def updateKeyword(keytext, username, keyword):
    shelfFile[keytext] = [keytool.encrypt(username), keytool.encrypt(keyword)]; 

def searchKeyword(criteria):
    if criteria in shelfFile:
        pyperclip.copy(keytool.decrypt(shelfFile[criteria][1]))
        print('Username is %s and password has been copied' % keytool.decrypt(shelfFile[criteria][0]))
    else:
        print('There is no account named ' + criteria)

def matchPassword():
    if user in shelfFile:
        keyword = keytool.decrypt(shelfFile[user], True)
        print(keyword)
        return pwd == keyword
    else:
        print('Username and password doesn\'t match')
        return False

if not matchPassword():
    sys.exit()

while True:
    printMenu()
    userInput = input()
    if userInput == "1":
        print('Add/Update Account'.center(30, "="))

        #ask for key and password
        print('Enter Account Name: ', end='')
        keytext = input()
        print('Enter Username: ', end='')
        username = input()
        print('Enter Password: ')
        keyword = getpass.getpass()

        #update data
        updateKeyword(keytext, username, keyword)
        print('Account has been updated successfully')
        
    elif userInput == "2":
        print('Search Account'.center(30, "="))
        print('Enter Account Name: ', end='')
        searchCriteria = input()
        #search
        searchKeyword(searchCriteria)
        print(''.center(30, "="))
    elif userInput == "3":
        break

shelfFile.close()
