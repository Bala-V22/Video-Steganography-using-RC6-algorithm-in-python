from stegano import lsb
from os.path import isfile,join
from helpers import *
import time                                                                 #install time ,opencv,numpy modules
import cv2
import numpy as np
import math
import os
video_name = 'video.avi'
import shutil
from subprocess import call,STDOUT 
from termcolor import cprint 
import moviepy.editor
from moviepy.editor import *
from werkzeug.utils import secure_filename
from PIL import Image 
import PIL 




def encrypt(sentence,s):
    encoded = blockConverter(sentence)
    enlength = len(encoded)
    A = int(encoded[0],2)
    B = int(encoded[1],2)
    C = int(encoded[2],2)
    D = int(encoded[3],2)
    orgi = []
    orgi.append(A)
    orgi.append(B)
    orgi.append(C)
    orgi.append(D)
    r=12
    w=32
    modulo = 2**32
    lgw = 5
    B = (B + s[0])%modulo
    D = (D + s[1])%modulo 
    for i in range(1,r+1):
        t_temp = (B*(2*B + 1))%modulo 
        t = ROL(t_temp,lgw,32)
        u_temp = (D*(2*D + 1))%modulo
        u = ROL(u_temp,lgw,32)
        tmod=t%32
        umod=u%32
        A = (ROL(A^t,umod,32) + s[2*i])%modulo 
        C = (ROL(C^u,tmod,32) + s[2*i+ 1])%modulo
        (A, B, C, D)  =  (B, C, D, A)
    A = (A + s[2*r + 2])%modulo 
    C = (C + s[2*r + 3])%modulo
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    return orgi,cipher
d=''
def decrypt(secret_dec,s):
    encoded = blockConverter(secret_dec)
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

def frame_extraction(files):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder="./tmp"
    print("[INFO] tmp directory is created")

    vidcap = cv2.VideoCapture("uploads/{}".format(files))
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1
    print("video encodesucess")    

def decframe_extraction(files):
    if not os.path.exists("./tmps"):
        os.makedirs("tmps")
    temp_folder="./tmps"
    print("[INFO] tmp directory is created")

    vidcap = cv2.VideoCapture(files)
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1
    print("video encodesucess")     

def encode_string(esentence,root="./tmp/"):
    files="{}{}.png".format(root,0)
    secret_enc=lsb.hide(files,esentence)
    secret_enc.save(files)
  

# def audio(files):
se='There is no data'
#     video = moviepy.editor.VideoFileClip("uploads/{}".format(files))
#     audio = video.audio
#     audio.write_audiofile("sample.mp3")
#     clip = VideoFileClip("finish.mov")
#     audioclip = AudioFileClip("sample.mp3")
#     videoclip = clip.set_audio(audioclip)


def con_video(files):

    image_folder = 'tmp'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height=720
    width=1280


    video = cv2.VideoWriter(video_name, 0, 30, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def decode_string(key,files):
    # files=files[ :-4]
    # files="{}.mp4".format(files)
    decframe_extraction(files)
    root="./tmp/"

    secret=[]
    # for i in range(len(os.listdir(root))):
    if files==video_name:
        f_name="{}{}.png".format(root,0)
        secret_dec=lsb.reveal(f_name)
        print(secret_dec)
        if secret_dec == None:
            print("none")
        secret.append(secret_dec)
        clean_tmp()

        # print(hidden_data)
        print ("DECRYPTION: ")
        #key='A WORD IS A WORD'
        # key =input("Enter Key(0-16 characters): ")
        if len(key) <16:
            key = key + " "*(16-len(key))
        key = key[:16]
                            
        print ("UserKey: "+key )
        s = generateKey(key)
        
        cipher,orgi = decrypt(secret_dec,s)
        sentence = deBlocker(orgi)
        print ("\nEncrypted String list: ",cipher)
        print ("Encrypted String: " + secret_dec)
        print ("Length of Encrypted String: ",len(secret_dec))

        print ("\nDecrypted String list: ",orgi)
        print ("Decrypted String: " + sentence )
        print ("Length of Decrypted String: ",len(sentence))
        clean_tmp()
        clean_tmps()
        return sentence,secret_dec
    else:
        clean_tmp()
        clean_tmps()
        return se,d

def clean_tmp(path="./tmp"):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print("[INFO] tmp files are cleaned up")
    except:
        print("[INFO] tmp files are cleaned up") 

def clean_tmps(path="./tmps"):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print("[INFO] tmp files are cleaned up")
    except:
        print("[INFO] tmp files are cleaned up")                

def vmain(key,input_string,files):
    # input_string = input("Enter the input string :")
    # f_name=input("Enter the name of video: ")
    print ("ENCRYPTION: ")
    #key='A WORD IS A WORD'
    # key = input("Enter Key(0-16 characters): ")
    if len(key) <16:
        key = key + " "*(16-len(key))
    key = key[:16]
                            
    print ("UserKey: "+key )
    s = generateKey(key)
    #sentence = 'I WORD IS A WORD'
    # sentence =input("Enter Sentence(0-16 characters): ")
    if len(input_string) <16:
        input_string = input_string + " "*(16-len(input_string))
    input_string = input_string[:16]

    orgi,cipher = encrypt(input_string,s)
    esentence = deBlocker(cipher)

    print ("\nInput String: "+input_string )
    print ("Original String list: ",orgi)
    print ("Length of Input String: ",len(input_string))

    print ("\nEncrypted String list: ",cipher)
    print ("Encrypted String: " + esentence)
    print ("Length of Encrypted String: ",len(esentence))
    # f = open("encrypted.txt", encoding="utf-8","w")
    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(esentence)
        f.close()
    frame_extraction(files)
    encode_string(esentence)
    con_video(files)
    return esentence,input_string,key
    # audio(files)
    # clean_tmp()





