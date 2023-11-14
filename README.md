# RandsomWare detection software

This Repo is dedicated to studying basic randsomware and developing similar applications, then making programs based in python to Scan the file and report any suspicious activity. This project is purely  for education purpopses to detect the threat of ransomware in any file, this is currently under the ideology that we know what attack is coming for simplification purposes. Creating an entire antivirus for any file is possible, but is quite simply out of our reach at this point.

## Contributors:
Abe Artus  
Elijah DeBruyne  
Zane Lesley

## To-Do
### Virus 2 (zane)
- [x] Hide file log file for virus 2
- [x] Make a way to upload the log file for virus 2 with encryption to a different network
- [x] Detection/prescan software for virus 2
- [ ] Real time detection (Hard, would require some sort of low level kernal system)
- [ ] Send key from server to virus
- [ ] Create kill/delete command from server to virus
- [ ] Be able to log multiple days instead of just one log file
- [ ] More checking of file from the detecter (including socket and attempt to get ip/host)
- [ ] See if any information about key is avaliable from detector
- [ ] Be able to hold more log files on server script.
- [ ] Experiment with what happens if the user turns the computer off.
- [ ] POSSIBLE: Expand virus to be able to monitor mouse movement, as well as be able to control both mouse and keyboard.

### Others:
Virus to do
- [X] Develop a simple in directory encyption malware in python
- [ ] Develop a virus that will go beyond its directory and change other files in Python
- [ ] Develop a similar virus to encrypt a directory in C 
- [ ] Develop a dir changng virus that will encrypt files in C

File scanner to-do
- [ ] Develop program to detect basic encryption malware from source file (.py)
- [ ] Detect the simple in directory encryption
- [ ] Detect malware in C
- [ ] Develop a way to detect ransomare inside of a executable c file EX: ./virus

## Virus 1:
This virus will encrypt all files in the directory it's attached too, it will print out the encrytion key but thats just incase we do something wrong...

## Virus 2:
This is a keylogger that will record the user's keystroke into a file called log.txt. It will then send this file to a different server (we are just using localhost) then will delete the original log file off the computer.
- For further information on code, here are some resources:
    1. [Basics of Logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial://www.example.com)
    2. [Basics of Keyboard Monitoring](https://pynput.readthedocs.io/en/latest/keyboard.html#reference)
    3. [Logging Config](https://docs.python.org/3/library/logging.config.html)
    4. [CBC Encryption](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode)
    5. [Socket](https://realpython.com/python-sockets/#background)

### Detection for Keylogger:
Uses a python AST to go through and look specific keywords that are used from the keylogger python file, to expand on this you would contiune to cover
all types of different keywords to do with keyboard monitoring and logging/writing things to a file.
- for further information on code, here are some resources:
    1. [AST Documentation](https://docs.python.org/3/library/ast.html#)




## Dependencies:
- [pynput](https://pypi.org/project/pynput/)
- [pycryptodome](https://pypi.org/project/pycryptodome/)