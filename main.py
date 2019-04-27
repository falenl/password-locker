#!python

import sys, getpass, shelve, pyperclip
from keytool import *
from user import *

userName = getpass.getuser()
shelfFile = shelve.open('data/data')

passed = False
while not passed:
    pwd = getpass.getpass("User Name : %s\nPassword:" % userName)
    keytool = Keytool(pwd)
    keytool.loadKeyFromFile('data/keyfile')
    user = User(userName, shelfFile, keytool)
    passed = user.matchPassword(pwd)

def printMenu():
    print('Menu'.center(30, "="))
    print('1. Enter/Update Account')
    print('2. Search Account')
    print('3. Account List')
    print('4. Exit')
    print(''.center(30, "="))
    print('Choose menu: ', end='')

def updateKeyword(keytext, username, keyword):
    shelfFile[keytext] = [keytool.encrypt(username), keytool.encrypt(keyword)]; 

def find(criteria):
    if criteria in shelfFile:
        return True
    else:
        return False

def searchKeyword(criteria):
    if criteria in shelfFile:
        pyperclip.copy(keytool.decrypt(shelfFile[criteria][1]))
        print('Username is "%s" and password has been copied' % keytool.decrypt(shelfFile[criteria][0]))
    else:
        print('There is no account named ' + criteria)
        
while True:
    printMenu()
    userInput = input()
    if userInput == "1":        
        print('Add/Update Account'.center(30, "="))

        #ask for key and password
        print('Enter Account Name: ', end='')
        keytext = input()
        if find(keytext):
            print('Account is already exist. Are you sure want to overwrite? (y/n)')
            yesno = input()
            if yesno.lower() == 'n':
                continue
        
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
        print('Account List'.center(30, "="))
        for key in shelfFile:
            if key != userName:
                print(key)
        print(''.center(30, "="))
        
    elif userInput == "4":
        break

    print('\n\n')

shelfFile.close()
