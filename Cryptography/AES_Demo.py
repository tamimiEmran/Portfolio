# AES Demo
from AES import AES
import utils
import numpy as np 
import os


plainText = b'This is a long text as a test input for AES_Demo.py for task 7 in the assignment'

# define the KEYS
key_128 = utils.random_key_generator(128) 
key_192 = utils.random_key_generator(192) 
key_256 = utils.random_key_generator(256) 

# Instantiate AES objects
aes_128 = AES(key_128)
aes_192 = AES(key_192)
aes_256 = AES(key_256)
my_aes = AES( b"0123456789ABCDEF" )


#%%
# Example on small text Data (ECB Mode)
print("=========AES-128 (small Msg, ECB)=========")
# plainText = b"This is a sample message that is encrypted using AES/ECB Mode"
print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_128 = aes_128.encrypt(plainText , utils.BC_mode.ECB)
print("128-bit Key :" , key_128)
print("AES-128 cipherText : ", cipherText_128)
DplainText = aes_128.decrypt(cipherText_128 , utils.BC_mode.ECB)
print("Dycrpted cipher Text : " , DplainText)
#%%
# Example on small text Data (CBC Mode)
print("=========AES-192 (Long Msg, CBC )=========")
# plainText = b"This is a sample message that is encrypted using AES/CBC Mode"
iv = utils.generate_random_iv(128);
# print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_192 = aes_192.encrypt(plainText , utils.BC_mode.CBC , iv)
print("192-bit Key :" , key_192)
print("AES-192 cipherText : ", cipherText_192)
DplainText = aes_192.decrypt(cipherText_192 , utils.BC_mode.CBC , iv)
print("Dycrpted cipher Text : " , DplainText)
#%%
print("=========AES-192 (Long Msg, CFB )=========")
# plainText = b"This is a sample message that is encrypted using AES/CBC Mode"
iv = utils.generate_random_iv(128);
# print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_192 = aes_192.encrypt(plainText , utils.BC_mode.CFB , iv)
print("192-bit Key :" , key_192)
print("AES-192 cipherText : ", cipherText_192)
DplainText = aes_192.decrypt(cipherText_192 , utils.BC_mode.CFB , iv)
print("Dycrpted cipher Text : " , DplainText)

#%%
print("=========AES-192 (Long Msg, CTR )=========")
# plainText = b"This is a sample message that is encrypted using AES/CBC Mode"
iv = utils.generate_random_iv(128);
# print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_192 = aes_192.encrypt(plainText , utils.BC_mode.CTR , iv)
print("192-bit Key :" , key_192)
print("AES-192 cipherText : ", cipherText_192)
DplainText = aes_192.decrypt(cipherText_192 , utils.BC_mode.CTR , iv)
print("Dycrpted cipher Text : " , DplainText)


#%%

# Example on Image Data (OFB Mode)
print("=========AES-256 (Img, OFB )=========")
plainText = utils.imread(os.path.dirname(os.path.abspath(__file__)) +'\\tiles.jpg')
utils.imshow_(plainText ,"Original Image")
size , plainText = utils.image2byte( plainText )
cipherText_256 = aes_256.encrypt(plainText , utils.BC_mode.OFB , iv)
print("256-bit Key :" , key_256)

utils.imshow_(utils.byte2image(size , cipherText_256[ :np.prod(size) ]) , "Encrypted Image")
#%%
DplainText = aes_256.decrypt(cipherText_256 , utils.BC_mode.OFB , iv)
DplainText = utils.byte2image(size , DplainText)
utils.imshow_(DplainText  , "Decrypted Image")
