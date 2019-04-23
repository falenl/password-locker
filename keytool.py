from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode, urlsafe_b64encode
import os, random, string

class Keytool:

    def __init__(self, pwd):
        self.pwd = pwd
        self.salt = ''
    
    def generateKey(self):
        print('Generating Key...')
        key = Fernet.generate_key()
        print('A key has been generated: ' + key.decode())
        return key
        
    def encrypt(self, strText, doubleSecure=False):
        print('Encrypting text...')
        if doubleSecure:
            strText = self.password_suite.encrypt(strText.encode())
        else:
            strText = strText.encode()
        ciphered_text = self.fernet_suite.encrypt(strText)
        print('Text encrypted.')
        return b64encode(self.salt + ciphered_text)

    def decrypt(self, encryptedText, doubleSecure=False):
        print('Decrypting text...')
        # Split out the salt from the ciphertext
        ciphertext = b64decode(encryptedText)
        self.salt = ciphertext[:16]
        ciphertext = ciphertext[16:]

        self.loadKey()
        unciphered_text = self.fernet_suite.decrypt(ciphertext)
        if doubleSecure:
            unciphered_text = self.password_suite.decrypt(unciphered_text)
        print('Text decrypted.')
        return unciphered_text.decode()

    def generateSalt(self, size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def loadKey(self):
        if (self.salt == ''):
            self.salt = self.generateSalt(16).encode()
        
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=self.salt,
                     iterations=100000,
                     backend=default_backend())
        key = urlsafe_b64encode(kdf.derive(self.pwd.encode()))
        
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

    
