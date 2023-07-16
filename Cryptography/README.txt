#############################################################################
# 				Documentation				    #
#############################################################################
#
# This is a full python implementation of DES, triple DES, AES, and RC4 encryption and 
# decryption algorithms using native python. The code also supports different
# key lengths for the AES and some useful utilities functions such as PKCS#7
# for padding and un-padding, random key generators, image pre-processing 
# functions, simple channel characterization, and error calculation methods. 
# Additionally, the code implements 3 Block cipher modes of operation being: 
# ECB, CBC & OFB. Finally, different Demo Scripts are provided to demonstrate 
# some of the code capabilities such as text and image encryption. 
#
#############################################################################
# 				Setup				            #
#############################################################################
# 1- Make sure you are using python 3.7.8 or newer
# 2- Install the dependencies using:
#	$ pip install -r requirements.txt
# 3- To reproduce the results and plots, run main.py
# 	Note: The execution of the code will be halted (stopped) till the figuers 
#             are closed !
#	$ python main.py
# 4- Other files can also be used, such that:	      			
#	DES_Demo.py : demo for the DES encryption (using small, large and image data) 
#                     with different Mode of Operation (i.e. ECB, CBC and OFB).
#	AES_Demo.py : demo for the AES encryption (using small, large and image data) 
#                     with different Mode of Operation (i.e. ECB, CBC and OFB) and 
#                     different key lengths. 
#	utils.py    : some useful utilities functions that is used across the code. 
#
#############################################################################
# 				Work By				            #
#############################################################################	
Emran Al Tamimi
#############################################################################
# 				References			            #
#############################################################################	
# This code was implemented with the help of these GitHub repositories:
# [1] https://github.com/gabrielmbmb/aes
# [2] https://github.com/boppreh/aes
# [3] https://github.com/dkushagra/DES-Python
# [4] https://gist.github.com/BlackRabbit-github
# Other theoretical Ref. are listed in the report. 