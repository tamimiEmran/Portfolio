from DES import DES
import utils
from tqdm import tqdm
### receive a list of three keys


class DES3(DES):
    
    def encrypt_block(self, plaintext):
        cipherText1 = self.d1.encrypt_block( plaintext)
        decryptedCipherText1WdifferentKey = self.d2.decrypt_block(cipherText1)
        cipherTextFinal = self.d3.encrypt_block(decryptedCipherText1WdifferentKey)
        return cipherTextFinal
    
    def decrypt_block(self, ciphertext):
        plainText1 = self.d3.decrypt_block(ciphertext)
        encryptedPlainTextWithDifferentKey = self.d2.encrypt_block(plainText1)
        plainTextFinal = self.d1.decrypt_block( encryptedPlainTextWithDifferentKey)
        
        return plainTextFinal
        
    def __init__(self, keys):
        self.k1, self.k2, self.k3 = keys
        
        self.d1 = DES(self.k1)
        self.d2 = DES(self.k2)
        self.d3 = DES(self.k3)
        
    
    def encrypt(self, plaintext, mode = utils.BC_mode.ECB , iv = None ):
        assert isinstance( mode, utils.BC_mode  )
        assert iv==None or len(iv)==8
        plaintext = utils.strToBytes(plaintext)

        plaintext = utils.pad(plaintext , 8)
        blocks = []

        if( mode == utils.BC_mode.CBC  and iv != None):
            previous = iv
            for plaintext_block in tqdm(utils.split_blocks(plaintext , block_size=8), desc="CBC encryption"):
                # CBC mode encrypt:
                block = self.encrypt_block(self.xor_bytes(plaintext_block, previous))
                blocks.append(block)
                previous = block
            ciphertext =  b''.join(blocks)
        elif( mode == utils.BC_mode.OFB  and iv != None ):
            previous = iv
            for plaintext_block in tqdm(utils.split_blocks(plaintext , block_size=8), desc="OFB encryption"):
                # OFB mode encrypt: plaintext_block XOR encrypt(previous)
                block = self.encrypt_block(previous)
                ciphertext_block = self.xor_bytes(plaintext_block, block)
                blocks.append(ciphertext_block)
                previous = block
            ciphertext =  b''.join(blocks)
        else:
            for plaintext_block in tqdm(utils.split_blocks(plaintext, block_size=8), desc="ECB encryption"):
                # ECB mode encrypt:
                block = self.encrypt_block(plaintext_block)
                blocks.append(block)
            ciphertext =  b''.join(blocks)

        return ciphertext
    
    def decrypt( self, ciphertext, mode = utils.BC_mode.ECB , iv = None, des3 = False):
        """
        Decrypts `ciphertext` with the given initialization vector (iv).

        """
        assert isinstance( mode, utils.BC_mode  )
        assert iv==None or len(iv)==8
        ciphertext = utils.strToBytes(ciphertext)
        # if des3:
        #     print('des 3 cipher text padding')
        #     ciphertext = utils.pad(ciphertext)
        blocks = [] 

        if( mode == utils.BC_mode.CBC and iv != None):

            previous = iv
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext, block_size=8), desc="CBC decryption"):
                # CBC mode decryption:
                blocks.append(self.xor_bytes( previous, self.decrypt_block(ciphertext_block)  ))
                previous = ciphertext_block
            plaintext =  utils.unpad( b''.join(blocks) ) ;

        elif( mode == utils.BC_mode.OFB  and iv != None ):
            previous = iv
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext, block_size=8), desc="OFB decryption"):
                # OFB mode decryption: plaintext_block XOR encrypt(previous)
                block = self.encrypt_block(previous)
                plaintext_block = self.xor_bytes(ciphertext_block, block)
                blocks.append(plaintext_block)
                previous = block
            plaintext =  utils.unpad( b''.join(blocks) )
        else:
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext, block_size=8), desc="ECB decryption"):
                # ECB mode encrypt:
                block = self.decrypt_block(ciphertext_block)
                blocks.append(block)
            plaintext =  utils.unpad(b''.join(blocks) )

        return plaintext 


