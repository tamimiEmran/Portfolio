import os
from PIL import Image, ImageFont, ImageDraw, ImageOps , ImageShow
import numpy as np
from enum import Enum
def random_key_generator(key_length):
    """
    Creates a random key with key_length bytes
    in hexadecimal and ASCII as bytes data type

    Paramaters
    ----------

    key_length : int
        Key length in bits

    Returns
    -------

    key : bytes
        Key as (ASCII or HEX) as bytes (if HEX is reresentable in ASCII then ASCII is prited o.w /x with HEX)
        This means A=>65 not 10 in decimal while /x_0a is 10 in decimal .
    """
    return os.urandom(key_length // 8)

def generate_random_iv(iv_length):
    """
    Paramaters
    ----------

    key_length : int
        Key length in bits
    """
    return random_key_generator(iv_length)

def inBin( toPrint ):
    """
    Returns the Binary representation of the input as str (for display ONLY!)

    toPrint is string => ASCII represenation
    toPrint is bytes => No / => ASCII  but with / HEX to BIN
    """
    if isinstance(toPrint,str):
        return " ".join(f"{ord(i):08b}" for i in toPrint)

    return " ".join(f"{(i):08b}" for i in toPrint)


def pad(plaintext , block_size=16 ):
    """
    Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
    Note that if the plaintext size is a multiple of 16,
    a whole block will be added.
    """
    padding_len = block_size - (len(plaintext) % block_size)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(plaintext):
    """
    Removes a PKCS#7 padding, returning the unpadded text and ensuring the
    padding was correct.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding) , "Error in unpadding !!!"
    return message

def split_blocks(message, block_size=16, require_padding=True):
    """
    block_size in byte.
    """
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

def imread(path):
    return np.asarray(Image.open(path))
import matplotlib.pyplot as plt

def imshow_(img , title1 = '' ):
    x = Image.fromarray(img)
    x = ImageOps.expand(x, border=20, fill=(255,255,255))

    draw = ImageDraw.Draw(x)
    
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except :
        font = ImageFont.load_default()

    draw.text((20, 0), title1 , fill = (0,0,0), font = font)
    # ImageShow.show(x)
    #matplotlib implementation
    # plt.ion()
    plt.imshow(img,cmap='gray')
    if ( title1 != None ):
        plt.title(title1)
    # plt.show(block = False)  
    # print("DONE Plotting")  
    # plt.ioff() 
    # plt.show()
    return plt

def image2byte(img):
    return img.shape , img.reshape((-1)).tobytes() ; 

def byte2image(size , b):
    return np.frombuffer(b, dtype= 'uint8').reshape(size); 


class BC_mode(Enum):
     ECB = 1
     CBC = 2
     OFB = 3
     CFB = 4
     CTR = 5

def strToBytes(txt):
    if isinstance(txt, str):
				# Only accept ascii unicode values.
        try:
            return txt.encode('ascii')
        except UnicodeEncodeError:
            pass
        raise ValueError("Des can only work with encoded strings, not Unicode.")
    return txt

def String_to_BitList( data):
        """Turn the string data, into a list of bits (1, 0)'s"""
        l = len(data) * 8
        result = [0] * l
        pos = 0
        for ch in data:
            i = 7
            while i >= 0:
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1

        return result

def BitList_to_String( data):
        """Turn the list of bits -> data, into a string""" 
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << (7 - (pos % 8))
            if (pos % 8) == 7:
                result.append(c)
                c = 0
            pos += 1
        return bytes(result)

def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))

def compare2arrays(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return (i!=j for i, j in zip(a, b))

from random import sample
def channelError(input, prb,blocksize = 16):
    #write the code here to add noise the input such that the noise array will have 1's with a probability prb
    # the input is an array of bits
    inputLenght = len(input)
    numberOfOnes = int( inputLenght * prb)
    
    noise = [0] * inputLenght
    indexesOfNoise = sample(range(inputLenght), numberOfOnes)
    for i in indexesOfNoise:
        noise[i] = 1
    
    
    return [x ^ y for x, y in zip(noise, input)]
def task4(string_binary, prb = 0.03):
    print('original text: ', string_binary)
    print('noisy text: ', BitList_to_String(channelError(String_to_BitList(string_binary), prb)))
    
def byteErrorRate(x,y):
    """
    Both x and y are bytes or ASCII Strings
    """
    # assert (len(x) == len(y)), "Inputs dose not have the same length !!"
    # x = strToBytes(x)
    # y = strToBytes(y)
    # temp = xor_bytes(x,y) ;
    # return (sum(c1 != c2 for c1, c2 in zip(x, y)))/len(x)
    return blockErrorRate(x,y,1)

def bitErrorRate(x,y):
    """
    Both x and y are bytes or ASCII Strings
    """
    assert (len(x) == len(y)), "Inputs dose not have the same length !!"
    x = strToBytes(x)
    y = strToBytes(y)
    temp = xor_bytes(x,y) 
    temp = String_to_BitList(temp)
    return (temp.count(1)) / len(temp)

def blockErrorRate(x,y,blockSize):
    """
    Both x and y are bytes or ASCII Strings
    Paramaters
    ----------
    x :  bytes
        input1 

    y :  bytes
        input2

    blockSize : int
        block Size in bytes
    """
    assert (len(x) == len(y)), "Inputs dose not have the same length !!"
    x = strToBytes(x)
    y = strToBytes(y)
    temp = xor_bytes(x,y) 
    temp = String_to_BitList(temp)
    temp = [temp[i:i+blockSize*8] for i in range(0,len(temp), blockSize*8)]
    counter = 0 ;
    for q in temp:
        if any(v != 0 for v in q):
            counter +=1 ;

    return counter/len(temp)

def pixelErrorRate(x,y):
    """
    Both x and y are bytes or ASCII Strings
    Paramaters
    ----------
    x :  bytes
        input1

    y :  bytes
        input2

    blockSize : int
        block Size in bytes
    """
    assert (len(x) == len(y)), "Inputs dose not have the same length !!"
    x = strToBytes(x)
    y = strToBytes(y)
    temp = compare2arrays(x,y)
    return sum(temp)/len(x)


# see = image2byte(imread(os.path.dirname(os.path.abspath(__file__)) + '\\tiles.jpg'))

# imshow(byte2image(see[0], ))



imagesList = []
for i in range(3):
    tempLst = []
    for j in range(4):
        
        tempLst.append(imread(os.path.dirname(os.path.abspath(__file__)) + '\\tiles.jpg'))
        
    imagesList.append(tempLst)

