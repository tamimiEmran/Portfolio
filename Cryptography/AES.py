"""
This is a pure python implementation of the Advanced Encryption Standard 
AES with support for keys lengths ( AES-128, AES-192, AES-256). 

Disclaimer !!
The following GItHub Repos. where used in this implemenation...
[1] https://github.com/boppreh/aes
[2] https://github.com/gabrielmbmb/aes

"""
################################################################################################
# Class: ciphers and deciphers the plaintext using the AES block cipher
#           with support to AES 128 and AES 192 and AES 256
# internal parameters:
#       plaintext: the plain text of arbitrary length e.g. 64 bits, or 8 characters
#       key: the cipher key of arbitrary length e.g. 64 bits or 8 characters
# Important functions:
#       encrypt_block: encrypt one block of size 128 bits or 16 bytes
#       encrypt: encrypt any stream e.g. arbitrary length text or image using AES
################################################################################################

import utils
from tqdm import tqdm
# from enum import Enum

# class BC_mode(Enum):
#      ECB = 1
#      CBC = 2
#      OFB = 3

## Lookup Tables 
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

class AES:
  
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}
    # Constructor
    def __init__(self, master_key):
        """
        Initializes the object with a given key.
        """
        assert len(master_key) in AES.rounds_by_key_size
        utils.strToBytes(master_key)
        self.n_rounds = AES.rounds_by_key_size[len(master_key)]
        self._key_matrices = self._expand_key(master_key)

    # Key Schedule
    def _expand_key(self, master_key):
        """
        Expands and returns a list of key matrices for the given master_key.
        """
        # Initialize round keys with raw key material.
        key_columns = self.bytes2matrix(master_key)
        iteration_size = len(master_key) // 4

        # Each iteration has exactly as many columns as the key material.
        columns_per_iteration = len(key_columns)
        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:  # (num_keys + 1) * 4 word per key
            # Copy previous word.
            word = list(key_columns[-1])

            # Perform schedule_core once every "row". ( G fun and xor)
            if len(key_columns) % iteration_size == 0:
                # Circular shift.
                word.append(word.pop(0))
                # Map to S-BOX.
                word = [s_box[b] for b in word]
                # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                # Run word through S-box in the fourth iteration when using a
                # 256-bit key.
                word = [s_box[b] for b in word]

            # XOR with equivalent word from previous iteration.
            word = self.xor_bytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        # Group key words in 4x4 byte matrices.
        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

    # main Encryption Loop
    def encrypt_block(self, plaintext):
        """
        Encrypts a single block of 16 byte long plaintext.
        """
        assert len(plaintext) == 16
  
        plain_state = self.bytes2matrix(plaintext)
        
        self.add_round_key(plain_state, self._key_matrices[0])

        for i in range(1, self.n_rounds):
            self.sub_bytes(plain_state)
            self.shift_rows(plain_state)
            self.mix_columns(plain_state)
            self.add_round_key(plain_state, self._key_matrices[i])

        self.sub_bytes(plain_state)
        self.shift_rows(plain_state)
        self.add_round_key(plain_state, self._key_matrices[-1])

        return self.matrix2bytes(plain_state)

    # main Decryption Loop
    def decrypt_block(self, ciphertext):
        """
        Decrypts a single block of 16 byte long ciphertext.
        """
        assert len(ciphertext) == 16

        cipher_state = self.bytes2matrix(ciphertext)

        self.add_round_key(cipher_state, self._key_matrices[-1])
        self.inv_shift_rows(cipher_state)
        self.inv_sub_bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            self.add_round_key(cipher_state, self._key_matrices[i])
            self.inv_mix_columns(cipher_state)
            self.inv_shift_rows(cipher_state)
            self.inv_sub_bytes(cipher_state)

        self.add_round_key(cipher_state, self._key_matrices[0])

        return self.matrix2bytes(cipher_state)

    # Encryption Function
    def encrypt( self, plaintext, mode =utils.BC_mode.ECB , iv = None ):
        """
        Encrypts `plaintext` with `key` using AES-128, an HMAC to verify integrity,
        and PBKDF2 to stretch the given key.

        The exact algorithm is specified in the module docstring.
        """
        assert isinstance( mode, utils.BC_mode  )
        assert iv==None or len(iv)==16
        utils.strToBytes(plaintext)
        plaintext = utils.pad(plaintext)
        blocks = [] 

        if( mode == utils.BC_mode.CBC  and iv != None):
            previous = iv
            for plaintext_block in tqdm(utils.split_blocks(plaintext), desc="CBC encryption"):
                # CBC mode encrypt:
                block = self.encrypt_block(self.xor_bytes(plaintext_block, previous))
                # print(len(block))
                blocks.append(block)
                previous = block
            ciphertext =  b''.join(blocks)
        elif( mode == utils.BC_mode.OFB  and iv != None ):
            previous = iv
            for plaintext_block in tqdm(utils.split_blocks(plaintext), desc="OFB encryption"):
                # OFB mode encrypt: plaintext_block XOR encrypt(previous)
                block = self.encrypt_block(previous)
                ciphertext_block = self.xor_bytes(plaintext_block, block)
                blocks.append(ciphertext_block)
                previous = block
            ciphertext =  b''.join(blocks)
        elif (mode == utils.BC_mode.CFB and iv != None):
            previous = iv
            s = 8
            #The plain text will be encrypted depending on the number of bits s
            for plaintext_block in tqdm(utils.split_blocks(plaintext, block_size=s ), desc="CFB encryption"):

                #encrypt block previous and choose s bytes
                block = self.encrypt_block(previous)[:s]
                #XOR block with the plain text to produce first cipher
                ciphertext_block = self.xor_bytes(block, plaintext_block)
                blocks.append(ciphertext_block)
                
                #now we must update the blocks for the next loop
                #The cipher block we just encrypted will take the LSB
                prev_ciphertext_block = ciphertext_block
                previous = previous[:s] + prev_ciphertext_block
            
            ciphertext = b''.join(blocks)
            
        elif (mode == utils.BC_mode.CTR and iv != None):
            previous = iv
            def iv_to_bytes(iv):
                #returns an integer represented in bytes as the first counter
                return b''.join([iv[i].to_bytes(1, byteorder = 'little') for i in range(len(iv))])
                
            number_in_bytes = iv_to_bytes(iv)
            def bytes_to_int(bytes):
                return int.from_bytes(bytes, byteorder = 'little')
            number_int = bytes_to_int(number_in_bytes)
            
            def int_to_bytes(int):
                return int.to_bytes(16, byteorder = 'little')
            
            for counter, plaintext_block in tqdm(enumerate(utils.split_blocks(plaintext)), desc="CTR encryption"):
                counter_block = number_int + counter
                counter_block = counter_block % 2**16
                
                counter_block_to_encrypt = int_to_bytes(counter_block)
                
                block = self.encrypt_block(counter_block_to_encrypt)
                ciphertext_block = self.xor_bytes(block, plaintext_block)
                
                blocks.append(ciphertext_block)
                
                
                # CTR mode encrypt: plaintext_block XOR encrypt(counter)
                # write the code for the counter mode here
            ciphertext = b''.join(blocks)
        else:
            for plaintext_block in tqdm(utils.split_blocks(plaintext), desc="ECB encryption"):
                # ECB mode encrypt:
                block = self.encrypt_block(plaintext_block)
                blocks.append(block)
            ciphertext =  b''.join(blocks)

        return ciphertext 

    # Decryption Function
    def decrypt( self, ciphertext, mode = utils.BC_mode.ECB, iv = None):
        """
        Decrypts `ciphertext` with the given initialization vector (iv).

        """
        assert isinstance( mode, utils.BC_mode  )
        assert iv==None or len(iv)==16
        utils.strToBytes(ciphertext)
        # ciphertext = utils.pad(ciphertext)
        blocks = [] 

        if( mode == utils.BC_mode.CBC and iv != None):

            previous = iv
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext), desc="CBC decryption"):
                # CBC mode decryption:
                blocks.append(self.xor_bytes( previous, self.decrypt_block(ciphertext_block)  ))
                previous = ciphertext_block
            plaintext =  utils.unpad( b''.join(blocks) ) ;

        elif( mode == utils.BC_mode.OFB  and iv != None ):
            previous = iv
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext), desc="OFB decryption"):
                # OFB mode decryption: plaintext_block XOR encrypt(previous)
                block = self.encrypt_block(previous)
                plaintext_block = self.xor_bytes(ciphertext_block, block)
                blocks.append(plaintext_block)
                previous = block
            plaintext =  utils.unpad( b''.join(blocks) )
        elif (mode == utils.BC_mode.CFB and iv != None):
            previous = iv
            s = 8
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext, block_size=s), desc="CFB decryption"):


                temp = self.encrypt_block(previous)[:s]
                plaintext_block = self.xor_bytes(ciphertext_block, temp)
                blocks.append(plaintext_block)
                previous = previous[:s] + ciphertext_block


            plaintext =  utils.unpad( b''.join(blocks) )
            
            
        elif (mode == utils.BC_mode.CTR and iv != None):
            previous = iv
            def iv_to_bytes(iv):
                #returns an integer represented in bytes as the first counter
                return b''.join([iv[i].to_bytes(1, byteorder = 'little') for i in range(len(iv))])
                
            number_in_bytes = iv_to_bytes(iv)
            def bytes_to_int(bytes):
                return int.from_bytes(bytes, byteorder = 'little')
            number_int = bytes_to_int(number_in_bytes)
            
            def int_to_bytes(int):
                return int.to_bytes(16, byteorder = 'little')
            
            for counter, ciphertext_block in tqdm(enumerate(utils.split_blocks(ciphertext)), desc="CTR encryption"):
                counter_block = number_int + counter
                counter_block = counter_block % 2**16
                
                counter_block_to_encrypt = int_to_bytes(counter_block)
                
                block = self.encrypt_block(counter_block_to_encrypt)
                plaintext_block = self.xor_bytes(block, ciphertext_block)
                
                blocks.append(plaintext_block)
                
                
                # CTR mode encrypt: ciphertext_block XOR encrypt(counter)
                # write the code for the counter mode here
            plaintext = utils.unpad( b''.join(blocks) )
        else:
            for ciphertext_block in tqdm(utils.split_blocks(ciphertext), desc="ECB decryption"):
                # ECB mode encrypt:
                block = self.decrypt_block(ciphertext_block)
                blocks.append(block)
            plaintext =  utils.unpad(b''.join(blocks) )

        return plaintext 

    # internal use Methods 
    def bytes2matrix(self,text):
        """ Converts a 16-byte array into a 4x4 matrix. """
        return [list(text[i:i+4]) for i in range(0, len(text), 4)]

    def matrix2bytes(self,matrix):
        """ Converts a 4x4 matrix into a 16-byte array.  """
        return bytes(sum(matrix, []))

    def xor_bytes(self,a, b):
        """ Returns a new byte array with the elements xor'ed. """
        return bytes(i^j for i, j in zip(a, b))

    def sub_bytes(self,s):
        """ Returns a permuted byte array with the elements according to the s-box. """
        for i in range(4):
            for j in range(4):
                s[i][j] = s_box[s[i][j]]

    def add_round_key(self,s, k):
        """ XOR the key and the statue. """
        for i in range(4):
            for j in range(4):
                s[i][j] ^= k[i][j]

    def shift_rows(self,s):
        """
        Opessite to the Convention and literature, s matrix is in the form
        [B0,B1,B2,B3;       rather than     [B0,B4,B8,B12;
         B4 ........]                        B1 ........]
        and then you take the columsn, so the shifts are diffrent with this new Structuer of matrix

        """
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

    # To prevent timing attacks, xtime must takes a fixed number of cycles, independently of the value of its argument
    # this is achieved by inserting dummy instructions should in the right
    xtime = lambda self, a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else ( (a << 1) )
    
    def mix_single_column(self,a):
    # see Sec 4.1.2 in The Design of Rijndael
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ self.xtime(a[0] ^ a[1])
        a[1] ^= t ^ self.xtime(a[1] ^ a[2])
        a[2] ^= t ^ self.xtime(a[2] ^ a[3])
        a[3] ^= t ^ self.xtime(a[3] ^ u)
        
    def mix_single_column(self, a):
        # see Sec 4.1.2 in The Design of Rijndael
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ self.xtime(a[0] ^ a[1])
        a[1] ^= t ^ self.xtime(a[1] ^ a[2])
        a[2] ^= t ^ self.xtime(a[2] ^ a[3])
        a[3] ^= t ^ self.xtime(a[3] ^ u)


    def mix_columns(self, s):
        for i in range(4):
            self.mix_single_column(s[i])

    def inv_sub_bytes(self,s):
        for i in range(4):
            for j in range(4):
                s[i][j] = inv_s_box[s[i][j]]

    def inv_shift_rows(self,s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

    def inv_mix_columns(self, s):
    # see Sec 4.1.3 in The Design of Rijndael
    # they notice that inv can be broken down to pre-processing and mix row !!! 
        for i in range(4):
            u = self.xtime(self.xtime(s[i][0] ^ s[i][2]))
            v = self.xtime(self.xtime(s[i][1] ^ s[i][3]))
            s[i][0] ^= u
            s[i][1] ^= v
            s[i][2] ^= u
            s[i][3] ^= v

        self.mix_columns(s)
