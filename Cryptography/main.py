import utils
from TxRxWrapper import tx, rx, CipherType
import os
from timeit import default_timer
import matplotlib.pyplot as plt
import numpy as np
import math
import customUtils 
from functools import wraps
from time import time


class images:
    monalisa100 = os.path.dirname(os.path.abspath(__file__)) + '\\monalisa100.jpg'
    monalisa200 = os.path.dirname(os.path.abspath(__file__)) + '\\monalisa200.jpg'
    monalisa300 = os.path.dirname(os.path.abspath(__file__)) + '\\monalisa300.jpg'
    monalisa400 = os.path.dirname(os.path.abspath(__file__)) + '\\monalisa400.jpg'



def compareCHERR_DES_AESx():
    #   use the following
    #       1- file monalisa200,
    #       2- the utility functions in utils file
    #       3- generate a key using the random generator in the utils file
    #   write the code here to compare "Pixel error rate" and "time complexity of the encryption" between DES, AES-128, AES-192, and AES-256
    #   for different channel error rates, including 10e-4 ,10e-5 , and 10e-6
    #   report the following output
    #       1- reslted image for all 12 cases
    #       2- a figure that shows the pixel error rate for each case vs the channel error rate
    #       3- a figure that shows the time complexity for each case vs the channel error rate

    trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"]
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    keys = [utils.random_key_generator(i) for i in [64, 128, 192, 256]]
    
    #cipherTypes
    cipherTypes = [CipherType.DES, CipherType.AES,CipherType.AES,CipherType.AES]
    
    #load size and image
    size, image = customUtils.loadimage(images.monalisa200)
    #encrypt using trial order (note that AES should be with its corresponding key in keys)
    #time it and return time
    
    imagesList = []
    pixelDistortions = []
    timeComplexity = []
    for errorRate in channelErr:
        imagesFixedError = []
        pixelFixedError = []
        timeFixedError = []
        for cipherType, key in zip(cipherTypes, keys):
            tStart = default_timer()
            encryptedImage = tx(image, key, cipherType)
            
            #apply noise
            noisyEncryptedImage = customUtils.add_noise_to_image(encryptedImage,errorRate )
            
            #decrypt cipher text
            decryptedImage_bytes = rx(noisyEncryptedImage, key, cipherType)
            
            #convert bytes to size and image
            decryptedImage = utils.byte2image(size, decryptedImage_bytes)
            # originalImage = utils.byte2image(size, image)
            
            #compare decrypted image with original !!!!Bytes
            distortion = utils.pixelErrorRate(image, decryptedImage_bytes)
            
            #append the resutls to be studied
            imagesFixedError.append(decryptedImage)
            pixelFixedError.append(distortion)
            tEnd = default_timer()
            timeFixedError.append(tEnd - tStart)
        
        imagesList.append(imagesFixedError)
        pixelDistortions.append(pixelFixedError)
        timeComplexity.append(timeFixedError)
        
    
    customUtils.plotImages(imagesList, len(channelErr), len(cipherTypes))
    # customUtils.plotDistortions(pixelDistortions)
    
    customUtils.plotTime(timeComplexity)
    customUtils.plotTime(pixelDistortions, name = 'Pxl_error_rate')
            
            
            
    
    
    
    
   
    
    
    
    
    #time it and compare it
    
    
    

def compareIMGQLTY_DES_AES_RC4():
    #   use the following
    #       1- files monalisa100, monalisa200, monalisa300, monalisa400
    #       2- the utility functions in utils file
    #       3- generate a key using the random generator in the utils file
    #   write the code here to compare "Pixel error rate" and "time complexity of the encryption" between DES, DES3, AES-128, and RC4
    #   for different channel error rates, including 10e-4 ,10e-5 , and 10e-6
    #   report the following output
    #       1- reslted image for all 12 cases
    #       2- a figure that shows the pixel error rate for each case vs the channel error rate

    # declare some list to Config. the experiment and save DATA !

    #cipherTypes
    
    
    enctyptionalgorithms = ["DES", "DES3", "AES-128", "RC4"]
    keys = [utils.random_key_generator(i) for i in [64, 64, 128, 64]]
    keys[1] = [utils.random_key_generator(i) for i in [64, 64, 64]]
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    cipherTypes = [CipherType.DES, CipherType.DES3,CipherType.AES,CipherType.RC4]
    timeComplexity_size = []
    pixelDistortions_size = []
    for imageMonalisaRes in [images.monalisa100, images.monalisa200,images.monalisa300,images.monalisa400]:
        size, image = customUtils.loadimage(imageMonalisaRes)
        #encrypt using trial order (note that AES should be with its corresponding key in keys)
        #time it and return time
        
        imagesList = []
        pixelDistortions = []
        timeComplexity = []
        for errorRate in channelErr:
            imagesFixedError = []
            pixelFixedError = []
            timeFixedError = []
            for cipherType, key in zip(cipherTypes, keys):
                tStart = default_timer()
                encryptedImage = tx(image, key, cipherType)
                
                #apply noise
                noisyEncryptedImage = customUtils.add_noise_to_image(encryptedImage,errorRate )
                
                #decrypt cipher text
                decryptedImage_bytes = rx(noisyEncryptedImage, key, cipherType)
                
                #convert bytes to size and image
                decryptedImage = utils.byte2image(size, decryptedImage_bytes)
                # originalImage = utils.byte2image(size, image)
                
                #compare decrypted image with original_ bytesss
                distortion = utils.pixelErrorRate(image, decryptedImage_bytes)
                
                #append the resutls to be studied
                imagesFixedError.append(decryptedImage)
                pixelFixedError.append(distortion)
                timeFixedError.append(default_timer() - tStart)
            
            imagesList.append(imagesFixedError)
            pixelDistortions.append(pixelFixedError)
            timeComplexity.append(timeFixedError)
            
        
        customUtils.plotImages(imagesList, len(channelErr), len(cipherTypes), number = str(imageMonalisaRes)[-7:-4], trialOrder = enctyptionalgorithms)
        timeComplexity_size.append(timeComplexity)
        pixelDistortions_size.append(pixelDistortions)
    customUtils.plotDistortions_vssize(pixelDistortions_size, len(channelErr), len(cipherTypes), enctyptionalgorithms)
    customUtils.plotTime_vssize(timeComplexity_size,len(channelErr), len(cipherTypes),enctyptionalgorithms)
    

def compareCHERR_AESmodes_RC4():
    #   use the following
    #       1- file monalisa200,
    #       2- the utility functions in utils file
    #       3- generate a key using the random generator in the utils file
    #   write the code here to compare "Pixel error rate" and "time complexity of the encryption" between DES, AES-128, AES-192, and AES-256
    #   for different channel error rates, including 10e-4 ,10e-5 , and 10e-6
    #   report the following output
    #       1- reslted image for all cases
    #       2- a figure that shows the pixel error rate for each case vs the channel error rate
    #       3- a figure that shows the time complexity for each case vs the channel error rate

    enctyptionalgorithms = ["AES", "AES-CBC", "AES-OFB", "AES-CFB", "AES-CTR", "RC4"]
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    keys = [utils.random_key_generator(i) for i in [128, 128, 128, 128, 128, 64]]
    IV = utils.generate_random_iv(8*16)
    
    cipherTypes = [(CipherType.AES, utils.BC_mode.ECB ),
                   (CipherType.AES, utils.BC_mode.CBC ),
                   (CipherType.AES, utils.BC_mode.OFB ),
                   (CipherType.AES, utils.BC_mode.CFB ),
                   (CipherType.AES, utils.BC_mode.CTR ),
                   (CipherType.RC4, utils.BC_mode.ECB ),
                   ]
    
    #load size and image
    size, image = customUtils.loadimage(images.monalisa200)
    #encrypt using trial order (note that AES should be with its corresponding key in keys)
    #time it and return time
    
    imagesList = []
    pixelDistortions = []
    timeComplexity = []
    for errorRate in channelErr:
        imagesFixedError = []
        pixelFixedError = []
        timeFixedError = []
        for cipherType, key in zip(cipherTypes, keys):
            tStart = default_timer()
            encryptedImage = tx(image, key, *cipherType,  IV )
            
            #apply noise
            noisyEncryptedImage = customUtils.add_noise_to_image(encryptedImage,errorRate )
            
            #decrypt cipher text
            decryptedImage_bytes = rx(noisyEncryptedImage, key, *cipherType, IV )
            
            #convert bytes to size and image
            decryptedImage = utils.byte2image(size, decryptedImage_bytes)
            # originalImage = utils.byte2image(size, image)
            
            #compare decrypted image with original !!!!Bytes
            distortion = utils.pixelErrorRate(image, decryptedImage_bytes)
            
            #append the resutls to be studied
            imagesFixedError.append(decryptedImage)
            pixelFixedError.append(distortion)
            tEnd = default_timer()
            timeFixedError.append(tEnd - tStart)
        
        imagesList.append(imagesFixedError)
        pixelDistortions.append(pixelFixedError)
        timeComplexity.append(timeFixedError)
        
    
    customUtils.plotImages(imagesList, len(channelErr), len(cipherTypes), trialOrder=enctyptionalgorithms, number= 200 )
    # customUtils.plotDistortions(pixelDistortions, trialOrder= enctyptionalgorithms)
    customUtils.plotTime(timeComplexity, trialOrder=enctyptionalgorithms)
    customUtils.plotTime(pixelDistortions, trialOrder= enctyptionalgorithms, name = 'pixel_error_rate')

def compareIMGQLTY_AESmodes_RC4():
    #   use the following
    #       1- files monalisa100, monalisa200, monalisa300, monalisa400
    #       2- the utility functions in utils file
    #       3- generate a key using the random generator in the utils file
    #   write the code here to compare "Pixel error rate" and "time complexity of the encryption" between DES, DES3, AES-128, and RC4
    #   for different channel error rates, including 10e-4 ,10e-5 , and 10e-6
    #   report the following output
    #       1- reslted image for all cases
    #       2- a figure that shows the pixel error rate for each case vs the channel error rate

    # declare some list to Config. the experiment and save DATA !
    enctyptionalgorithms = ["AES", "AES-CBC", "AES-OFB", "AES-CFB", "AES-CTR", "RC4"]
    keys = [utils.random_key_generator(i) for i in [128, 128, 128, 128, 128, 128]]
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    
    IV = utils.generate_random_iv(8*16)
    
    cipherTypes = [(CipherType.AES, utils.BC_mode.ECB ),
                   (CipherType.AES, utils.BC_mode.CBC ),
                   (CipherType.AES, utils.BC_mode.OFB ),
                   (CipherType.AES, utils.BC_mode.CFB ),
                   (CipherType.AES, utils.BC_mode.CTR ),
                   (CipherType.RC4, utils.BC_mode.ECB ),
                   ]
    
    timeComplexity_size = []
    pixelDistortions_size = []
    for imageMonalisaRes in [images.monalisa100, images.monalisa200,images.monalisa300,images.monalisa400]:
        size, image = customUtils.loadimage(imageMonalisaRes)
        #encrypt using trial order (note that AES should be with its corresponding key in keys)
        #time it and return time
        
        imagesList = []
        pixelDistortions = []
        timeComplexity = []
        for errorRate in channelErr:
            imagesFixedError = []
            pixelFixedError = []
            timeFixedError = []
            for cipherType, key in zip(cipherTypes, keys):
                tStart = default_timer()
                encryptedImage = tx(image, key, *cipherType, IV)
                
                #apply noise
                noisyEncryptedImage = customUtils.add_noise_to_image(encryptedImage,errorRate )
                
                #decrypt cipher text
                decryptedImage_bytes = rx(noisyEncryptedImage, key, *cipherType, IV)
                
                #convert bytes to size and image
                decryptedImage = utils.byte2image(size, decryptedImage_bytes)
                # originalImage = utils.byte2image(size, image)
                
                #compare decrypted image with original_ bytesss
                distortion = utils.pixelErrorRate(image, decryptedImage_bytes)
                
                #append the resutls to be studied
                imagesFixedError.append(decryptedImage)
                pixelFixedError.append(distortion)
                
                timeFixedError.append(default_timer() - tStart)
                # print( '\n ================ \n', cipherType, errorRate, default_timer() - tStart,'================\n')
            
            imagesList.append(imagesFixedError)
            pixelDistortions.append(pixelFixedError)
            timeComplexity.append(timeFixedError)
            
        
        customUtils.plotImages(imagesList, len(channelErr), len(cipherTypes), number = str(imageMonalisaRes)[-7:-4], trialOrder = enctyptionalgorithms)
        timeComplexity_size.append(timeComplexity)
        pixelDistortions_size.append(pixelDistortions)
    customUtils.plotDistortions_vssize(pixelDistortions_size, len(channelErr), len(cipherTypes),enctyptionalgorithms )
    customUtils.plotTime_vssize(timeComplexity_size, len(channelErr), len(cipherTypes),enctyptionalgorithms )

# compareCHERR_DES_AESx()
compareIMGQLTY_DES_AES_RC4()
# compareCHERR_AESmodes_RC4()
compareIMGQLTY_AESmodes_RC4()
