################################################################################################
# Class: ciphers and deciphers the plaintext using the RC4 stream cipher to create a rc4text
# internal parameters:
#       plaintext: the plain text of arbitrary length e.g. 128 bits, or 16 characters
#       key: the cipher key of arbitrary length e.g. 64 bits or 8 characters
# Important functions:
#       KSA: perform the initial permutation for the random stream generator
#       PRGA: Pseudo random generator for arbitrary length random stream
#       encrypt: encrypt any stream e.g. arbitrary length text or image using RC4
################################################################################################
from utils import strToBytes
class RC4:
    def __init__(self, key):
        self.key= key

    def KSA(self, key):
        keylen = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % keylen]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def PRGA(self, n):
        i = 0
        j = 0
        RS = []
        self.S = self.KSA(self.key)
        while n > 0:
            n -= 1
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            RS.append(K)
        return RS

    def encrypt(self, plaintext):
        plaintext = strToBytes(plaintext)
        return b''.join([bytes([a ^ b]) for a, b in zip(plaintext, self.PRGA(len(plaintext)))])

    def decrypt(self, ciphertext):
        return b''.join([bytes([a ^ b]) for a, b in zip(ciphertext, self.PRGA(len(ciphertext)))])




