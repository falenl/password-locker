from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
import os, random, string

class Keytool:   
    
    def generateKey(self):
        print('Generating Key...')
        key = Fernet.generate_key()
        print('A key has been generated: ' + key.decode())
        return key
        
    def encrypt(self, strText, doubleSecure=False):
        print('Encrypting text...')
        if doubleSecure:
            strText = self.password_suite.encrypt(strText.encode())
        ciphered_text = self.fernet_suite.encrypt(strText)
        print('Text encrypted.')
        return ciphered_text

    def decrypt(self, encryptedText, doubleSecure=False):
        print('Decrypting text...')
        unciphered_text = self.fernet_suite.decrypt(encryptedText)
        if doubleSecure:
            unciphered_text = self.password_suite.decrypt(encryptedText)
        print('Text decrypted.')
        return unciphered_text.decode()

    def generateSalt(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def loadKey(self, password):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=self.generateSalt().encode(),
                     iterations=100000,
                     backend=default_backend())
        key = urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet_suite = Fernet(key)
       
    def loadKeyFromFile(self, filepath):
        #Read Key from keyfile

        if os.path.exists(filepath):
            #open file and get key
            keyFile = open(filepath)
            keyTemp = keyFile.read()
            key = keyTemp.encode()
        else:
            #generate and save key if it doesn't exist
            keyFile = open(filepath, 'w')
            key = self.generateKey()
            keyFile.write(key.decode())

        self.password_suite = Fernet(key)
        keyFile.close()

    
