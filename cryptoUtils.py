import base64
from Crypto.Cipher import AES
from Crypto import Random
from cryptography.hazmat.primitives import padding


BS = 0

def pad(data):
    # create instance of padder
    padder = padding.PKCS7(BS*8).padder()
    return padder.update(data) + padder.finalize()
	
def unpad(data):
	unpadder = padding.PKCS7(BS*8).unpadder()
	return unpadder.update(data) + unpadder.finalize()
	

class AESCipher:
	def __init__( self, key ,blockSize):
		# Expand or Shorten key based on the aes blocksize
		while (len(key) < blockSize):
			key += key

		key = key[:blockSize]
		self.key = key
		self.blockSize = blockSize
		global BS
		BS = blockSize
		#Block size will be either 16 or 31 according to AES128 or AES256 respectively, or 0 if none

	def createIV(self):
		return Random.new().read(AES.block_size)

	def encrypt( self, mess ,IV):
		if BS == 0:
			#print("printed: " + mess.decode("ascii"))
			return mess
		mess=pad(mess)
		cipher = AES.new( self.key, AES.MODE_CBC, IV )
		return cipher.encrypt(mess)
		

	def decrypt( self, ciph ,IV):
		if BS == 0:
			return ciph
		cipher = AES.new(self.key, AES.MODE_CBC, IV)
		paddedPlain = cipher.decrypt(ciph)
		return unpad(paddedPlain)
		
	
	
