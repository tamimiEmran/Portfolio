import unittest
from AES import AES
from utils import BC_mode
"""
based on "https://github.com/boppreh/aes/test.py" implemenattion of AES test.
"""
class TestBlock(unittest.TestCase):
    """
    Tests raw AES-128 block operations.
    """
    def setUp(self):
        self.aes = AES(b'\x00' * 16)

    def test_success(self):
        """ Should be able to encrypt and decrypt block messages. """
        message = b'\x01' * 16
        ciphertext = self.aes.encrypt_block(message)
        self.assertEqual(self.aes.decrypt_block(ciphertext), message)

        message = b'a secret message'
        ciphertext = self.aes.encrypt_block(message)
        self.assertEqual(self.aes.decrypt_block(ciphertext), message)

    def test_bad_key(self):
        """ Raw AES requires keys of an exact size. """
        with self.assertRaises(AssertionError):
            AES(b'short key')

        with self.assertRaises(AssertionError):
            AES(b'long key' * 10)

    def test_expected_value(self):
        """
        Tests taken from the NIST document, Appendix B:
        http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        """
        message = b'\x32\x43\xF6\xA8\x88\x5A\x30\x8D\x31\x31\x98\xA2\xE0\x37\x07\x34'
        key     = b'\x2B\x7E\x15\x16\x28\xAE\xD2\xA6\xAB\xF7\x15\x88\x09\xCF\x4F\x3C'
        ciphertext = AES(bytes(key)).encrypt_block(bytes(message))
        self.assertEqual(ciphertext, b'\x39\x25\x84\x1D\x02\xDC\x09\xFB\xDC\x11\x85\x97\x19\x6A\x0B\x32')

class TestKeySizes(unittest.TestCase):
    """
    Tests encrypt and decryption using 192- and 256-bit keys.
    """
    def test_192(self):
        aes = AES(b'P' * 24)
        message = b'M' * 16
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_256(self):
        aes = AES(b'P' * 32)
        message = b'M' * 16
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_expected_values192(self):
        message = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
        aes = AES(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17')
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(ciphertext, b'\xdd\xa9\x7c\xa4\x86\x4c\xdf\xe0\x6e\xaf\x70\xa0\xec\x0d\x71\x91')
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_expected_values256(self):
        message = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
        aes = AES(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f')
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(ciphertext, b'\x8e\xa2\xb7\xca\x51\x67\x45\xbf\xea\xfc\x49\x90\x4b\x49\x60\x89')
        self.assertEqual(aes.decrypt_block(ciphertext), message)


class TestCbc(unittest.TestCase):
    """
    Tests AES-128 in CBC mode.
    """
    def setUp(self):
        self.aes = AES(b'\x00' * 16)
        self.iv = b'\x01' * 16
        self.message = b'my message'

    def test_single_block(self):
        """ Should be able to encrypt and decrypt single block messages. """
        ciphertext = self.aes.encrypt(self.message, BC_mode.CBC ,self.iv)
        self.assertEqual(self.aes.decrypt(ciphertext, BC_mode.CBC , self.iv), self.message)

        # Since len(message) < block size, padding won't create a new block.
        self.assertEqual(len(ciphertext), 16)

    def test_wrong_iv(self):
        """ CBC mode should verify the IVs are of correct length."""
        with self.assertRaises(AssertionError):
            self.aes.encrypt(self.message,  BC_mode.CBC  ,b'short iv')

        with self.assertRaises(AssertionError):
            self.aes.encrypt(self.message,  BC_mode.CBC ,b'long iv' * 16)

        with self.assertRaises(AssertionError):
            self.aes.decrypt(self.message, BC_mode.CBC , b'short iv')

        with self.assertRaises(AssertionError):
            self.aes.decrypt(self.message,  BC_mode.CBC ,b'long iv' * 16)

    def test_different_iv(self):
        """ Different IVs should generate different ciphertexts. """
        iv2 = b'\x02' * 16

        ciphertext1 = self.aes.encrypt(self.message,  BC_mode.CBC ,self.iv)
        ciphertext2 = self.aes.encrypt(self.message, BC_mode.CBC , iv2)
        self.assertNotEqual(ciphertext1, ciphertext2)

        plaintext1 = self.aes.decrypt(ciphertext1,  BC_mode.CBC ,self.iv)
        plaintext2 = self.aes.decrypt(ciphertext2,  BC_mode.CBC ,iv2)
        self.assertEqual(plaintext1, plaintext2)
        self.assertEqual(plaintext1, self.message)

    def test_whole_block_padding(self):
        """ When len(message) == block size, padding will add a block. """
        block_message = b'M' * 16
        ciphertext = self.aes.encrypt(block_message,  BC_mode.CBC ,self.iv)
        self.assertEqual(len(ciphertext), 32)
        self.assertEqual(self.aes.decrypt(ciphertext, BC_mode.CBC , self.iv), block_message)

    def test_long_message(self):
        """ CBC should allow for messages longer than a single block. """
        long_message = b'M' * 100
        ciphertext = self.aes.encrypt(long_message,  BC_mode.CBC ,self.iv)
        self.assertEqual(self.aes.decrypt(ciphertext,  BC_mode.CBC ,self.iv), long_message)


class TestOfb(unittest.TestCase):
    """
    Tests AES-128 in CBC mode.
    """
    def setUp(self):
        self.aes = AES(b'\x00' * 16)
        self.iv = b'\x01' * 16
        self.message = b'my message'

    def test_single_block(self):
        """ Should be able to encrypt and decrypt single block messages. """
        ciphertext = self.aes.encrypt(self.message, BC_mode.OFB, self.iv)
        self.assertEqual(self.aes.decrypt(ciphertext, BC_mode.OFB, self.iv), self.message)

        # self.assertEqual(len(ciphertext), len(self.message))

    def test_wrong_iv(self):
        """ CBC mode should verify the IVs are of correct length."""
        with self.assertRaises(AssertionError):
            self.aes.encrypt(self.message,BC_mode.OFB, b'short iv')

        with self.assertRaises(AssertionError):
            self.aes.encrypt(self.message,BC_mode.OFB, b'long iv' * 16)

        with self.assertRaises(AssertionError):
            self.aes.decrypt(self.message, BC_mode.OFB ,b'short iv')

        with self.assertRaises(AssertionError):
            self.aes.decrypt(self.message, BC_mode.OFB , b'long iv' * 16)

    def test_different_iv(self):
        """ Different IVs should generate different ciphertexts. """
        iv2 = b'\x02' * 16

        ciphertext1 = self.aes.encrypt(self.message, BC_mode.OFB ,self.iv)
        ciphertext2 = self.aes.encrypt(self.message, BC_mode.OFB, iv2)
        self.assertNotEqual(ciphertext1, ciphertext2)

        plaintext1 = self.aes.decrypt(ciphertext1, BC_mode.OFB,  self.iv)
        plaintext2 = self.aes.decrypt(ciphertext2, BC_mode.OFB, iv2)
        self.assertEqual(plaintext1, plaintext2)
        self.assertEqual(plaintext1, self.message)

    def test_whole_block_padding(self):
        """ When len(message) == block size, padding will add a block. """
        block_message = b'M' * 16
        ciphertext = self.aes.encrypt(block_message,BC_mode.OFB, self.iv)
        self.assertNotEqual(len(ciphertext), len(block_message))
        self.assertEqual(self.aes.decrypt(ciphertext,BC_mode.OFB, self.iv), block_message)

    def test_long_message(self):
        """ CBC should allow for messages longer than a single block. """
        long_message = b'M' * 100
        ciphertext = self.aes.encrypt(long_message, BC_mode.OFB, self.iv)
        self.assertEqual(self.aes.decrypt(ciphertext,BC_mode.OFB, self.iv), long_message)


def run():
    unittest.main()

if __name__ == '__main__':
    run()