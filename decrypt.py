from helpers import *
import sys
from PIL import Image
from stegano import lsb



def decrypt(esentence,s):
    encoded = blockConverter(esentence)
    enlength = len(encoded)
    A = int(encoded[0],2)
    B = int(encoded[1],2)
    C = int(encoded[2],2)
    D = int(encoded[3],2)
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    r=12
    w=32
    modulo = 2**32
    lgw = 5
    C = (C - s[2*r+3])%modulo
    A = (A - s[2*r+2])%modulo
    for j in range(1,r+1):
        i = r+1-j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D*(2*D + 1))%modulo
        u = ROL(u_temp,lgw,32)
        t_temp = (B*(2*B + 1))%modulo 
        t = ROL(t_temp,lgw,32)
        tmod=t%32
        umod=u%32
        C = (ROR((C-s[2*i+1])%modulo,tmod,32)  ^u)  
        A = (ROR((A-s[2*i])%modulo,umod,32)   ^t) 
    D = (D - s[1])%modulo 
    B = (B - s[0])%modulo
    orgi = []
    orgi.append(A)
    orgi.append(B)
    orgi.append(C)
    orgi.append(D)
    return cipher,orgi



def dmain(key,file):
    hidden_data=lsb.reveal("images\{}".format(file))

    print(hidden_data)
    print ("DECRYPTION: ")
    #key='A WORD IS A WORD'
    # key =input("Enter Key(0-16 characters): ")
    if len(key) <16:
        key = key + " "*(16-len(key))
    key = key[:16]
                         
    print ("UserKey: "+key )
    s = generateKey(key)
    
    cipher,orgi = decrypt(hidden_data,s)
    sentence = deBlocker(orgi)
    print ("\nEncrypted String list: ",cipher)
    print ("Encrypted String: " + hidden_data)
    print ("Length of Encrypted String: ",len(hidden_data))

    print ("\nDecrypted String list: ",orgi)
    print ("Decrypted String: " + sentence )
    print ("Length of Decrypted String: ",len(sentence))
    return hidden_data,sentence
    

# if __name__ == "__main__":
#     main()
