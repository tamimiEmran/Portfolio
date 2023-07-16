
from DES3 import DES3
import utils
import numpy as np 
import os 
from textEx import text as pt


# define the KEYS
keys = [utils.random_key_generator(64) for i in range(3)]
print(len(keys[0]))

# Instantiate AES objects
my_Des = DES3(keys)
#%%
# Example on small text Data (ECB Mode)
print("=========DES(small Msg, ECB)=========")
plainText = b"This is a test input for DES3 similar to task 1"
print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_1 = my_Des.encrypt(plainText , utils.BC_mode.ECB)
print("64-bit Key :" , keys)
print("DES cipherText : ", cipherText_1 )
DplainText = my_Des.decrypt(cipherText_1 , utils.BC_mode.ECB)
print("Dycrpted cipher Text : " , DplainText)
#%%
# # Example on Big text Data (CBC Mode)
print("=========DES (Long Msg, CBC )=========")
# plainText = b"This is a sample message that is encrypted using DES/CBC Mode"
iv = utils.generate_random_iv(64);
print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_2 = my_Des.encrypt(plainText , utils.BC_mode.CBC , iv)
print("64-bit Key :" , keys)
print("DES cipherText : ", cipherText_2)
DplainText = my_Des.decrypt(cipherText_2 , utils.BC_mode.CBC , iv)
print("Dycrpted cipher Text : " , DplainText)
#%%

# Example on Image Data (OFB Mode)
print("=========DES (Img, OFB )=========")
plainText = utils.imread(os.path.dirname(os.path.abspath(__file__)) + '\\tiles.jpg')
utils.imshow_(plainText ,"Original Image")
size , plainText = utils.image2byte( plainText )
cipherText_3 = my_Des.encrypt(plainText , utils.BC_mode.OFB , iv)
# print("64-bit Key :" , key)

utils.imshow_(utils.byte2image(size , cipherText_3[ :np.prod(size) ]) , "Encrypted Image")

DplainText = my_Des.decrypt(cipherText_3 , utils.BC_mode.OFB , iv)
DplainText = utils.byte2image(size , DplainText)
utils.imshow_(DplainText  , "Decrypted Image")

