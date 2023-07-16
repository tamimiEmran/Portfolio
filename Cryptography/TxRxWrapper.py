
from AES import AES
from DES import DES
from DES3 import DES3
from RC4 import RC4
from enum import Enum
import utils
from functools import wraps
from time import time

def timeIt(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:%r took: %2.4f sec' %(f.__name__, ti := te-ts))
        return result, ti
    return wrap

class CipherType(Enum):
    DES = 1
    AES = 2
    DES3= 3
    RC4 = 4


def tx(input, key , cipher_type, bc_mode = utils.BC_mode.ECB , iv = None):
    assert isinstance(cipher_type,CipherType)
    assert isinstance(bc_mode,utils.BC_mode)

    if cipher_type == CipherType.DES:
        myDES = DES(key)
        return myDES.encrypt(input,bc_mode, iv)

    elif cipher_type == CipherType.AES:
        myAES = AES(key)
        return myAES.encrypt(input,bc_mode, iv)
    elif cipher_type == CipherType.DES3:
        myDES3 = DES3(key)
        return myDES3.encrypt(input,bc_mode, iv)
    elif cipher_type == CipherType.RC4:
        myRC4 = RC4(key)
        return myRC4.encrypt(input)

    else:
        raise Exception('Error')
        
        

def rx(input, key , cipher_type,bc_mode = utils.BC_mode.ECB , iv = None):
    assert isinstance(cipher_type,CipherType)
    assert isinstance(bc_mode,utils.BC_mode)

    if cipher_type == CipherType.DES:
        myDES = DES(key)
        return myDES.decrypt(input,bc_mode, iv)

    elif cipher_type == CipherType.AES:
        myAES = AES(key)
        return myAES.decrypt(input,bc_mode, iv)

    elif cipher_type == CipherType.DES3:
        myDES3 = DES3(key)
        return myDES3.decrypt(input,bc_mode, iv)

    elif cipher_type == CipherType.RC4:
        myRC4 = RC4(key)
        return myRC4.decrypt(input)

    else:
        raise Exception('Error')
