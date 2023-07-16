from RC4 import RC4
plaintext = "Hello, world!"
key = b'Secret key'
rc4_cipher = RC4(key)
ciphertext = rc4_cipher.encrypt(plaintext)





print('original text: ', plaintext)
print('cipher text: ' , ciphertext)
print('decoded text: ', rc4_cipher.encrypt(ciphertext))



import utils
import numpy as np 
import os 



# define the KEYS
key = utils.random_key_generator(64)


# Instantiate AES objects
rc4_cipher = RC4(key)
#%%
# Example on small text Data (ECB Mode)
print("=========RC4=========")
plainText = b"This is a test input for RC4 similar to task 1"
print("PlainText : " , plainText , " ==In Binary>> " , utils.inBin(plainText) )
cipherText_1 = rc4_cipher.encrypt(plainText)
print("64-bit Key :" , key)
print("DES cipherText : ", cipherText_1 )
DplainText = rc4_cipher.decrypt(cipherText_1)
print("Dycrpted cipher Text : " , DplainText)

#%%

# Example on Image Data (OFB Mode)
print("=========DES (Img, OFB )=========")
plainText = utils.imread(os.path.dirname(os.path.abspath(__file__)) + '\\tiles.jpg')
utils.imshow_(plainText ,"Original Image")
size , plainText = utils.image2byte( plainText )
cipherText_3 = rc4_cipher.encrypt(plainText)
# print("64-bit Key :" , key)

utils.imshow_(utils.byte2image(size , cipherText_3[ :np.prod(size) ]) , "Encrypted Image")
#%%
DplainText = rc4_cipher.decrypt(cipherText_3)
DplainText = utils.byte2image(size , DplainText)
utils.imshow_(DplainText  , "Decrypted Image")

