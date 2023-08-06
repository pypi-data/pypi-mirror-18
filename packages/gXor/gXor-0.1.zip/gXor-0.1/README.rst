XOR symmetric encryption method to secure the "imposition" of a sequence consisting of random numbers on the plaintext.
The sequence of random numbers is called the gamma-sequence and is used to encrypt or decrypt data.

Example:

import gXor

g = gXor.Gamma()

enc = g.crypt("Hi, my name is ... !", "asd123")
print (enc)
>>> �7az���c���.�h� 019

dec = g.decrypt(enc, "123asd")
print (dec)
>>> hi, my name is ...!

enc = g.crypt("������, ��� ���� �����?", "123���4")
print (enc)
>>> ikd��61ze4�g6a3z.���pl2

dec = g.decrypt(enc, "123���4")
print (dec)
>>> ������, ��� ���� �����?