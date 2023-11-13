# RandsomWare detection software

This Repo is dedicated to studying basic randsomare and developing similar applications, then making programs to Scan the file and report any suspicious activity. It is purely  for education purpopses to detect the threat of ransomware in any file.

## Contributors:
Abe Artus  
Elijah DeBruyne  
Zane Lesley

## To-Do
- [x] Hide file log file for virus 2 (zane)
- [] Make a way to upload the log file for virus 2 with encryption to a different network(zane) 
- [] Detection/prescan software for virus 2 (zane)
- [] real time detection (Hard, would require some sort of low level kernal system)

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
This is a keylogger that will record the user's keystroke into a file called log.txt
- for further information on code, here are some resources:
    1. [basics of logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial://www.example.com)
    2. [basics of the keyboard monitoring](https://pynput.readthedocs.io/en/latest/keyboard.html#reference)
    3. [logging config](https://docs.python.org/3/library/logging.config.html)

## Dependencies:
[pynput](https://pypi.org/project/pynput/)