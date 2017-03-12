import base64
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE=0



class AESCipher:
    def __init__( self, key ,blockSize):
        self.key = key
        self.blockSize = blockSize

    def createIV(self):
        return Random.new().read(self.blockSize)

    def encrypt( self, mess ,IV):
        length = self.blockSize - (len(mess) % self.blockSize)
        mess += chr(length) * length
        cipher = AES.new( self.key, AES.MODE_CBC, IV )
        return base64.b64encode(cipher.encrypt(mess))

    def decrypt( self, ciph ,IV):
        ciph = base64.b64decode(ciph)
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        ciph = ciph[:-ciph[-1]]
        return cipher.decrypt(ciph)