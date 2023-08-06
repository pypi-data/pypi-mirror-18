XOR symmetric encryption method to secure the "imposition" of a sequence consisting of random numbers on the plaintext.
The sequence of random numbers is called the gamma-sequence and is used to encrypt or decrypt data.

Example:

import gXor

g = gXor.Gamma()

enc = g.crypt("Hi, my name is ... !", "asd123")
print (enc)
>>> х7azтядcсск.цhж 019

dec = g.decrypt(enc, "123asd")
print (dec)
>>> hi, my name is ...!

enc = g.crypt("Привет, как тебя зовут?", "123апу4")
print (enc)
>>> ikdгх61ze4лg6a3z.ияцpl2

dec = g.decrypt(enc, "123апу4")
print (dec)
>>> привет, как тебя зовут?