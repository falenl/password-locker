#!python

class User:

    def __init__(self, username, shelfFile, keytool):
        self.username = username
        self.shelfFile = shelfFile
        self.keytool = keytool

    def matchPassword(self, pwd):
        if self.username in self.shelfFile:
            try:
                keyword = self.keytool.decrypt(self.shelfFile[self.username], True)
                return pwd == keyword
            except:
                print('Username and password doesn\'t match')        
        else:
            print('Username and password doesn\'t match')
            return False

    def changePassword(self, keytool):
        keytool2 = keytool
        #change all accounts in the shelf file
        for key in self.shelfFile:
            if key != self.username:
                account = self.shelfFile[key]
                user, pwd = self.keytool.decrypt(account[0]), self.keytool.decrypt(account[1])
                self.shelfFile[key] = [keytool2.encrypt(user), keytool2.encrypt(pwd)];
