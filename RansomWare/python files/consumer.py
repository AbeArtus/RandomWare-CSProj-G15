import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

#Server config
HOST = "localhost"
PORT = 9999

#Matches key from producer
key = b"Key For Testing."
cipher = AES.new(key, AES.MODE_CBC)

#Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

client, addr = server.accept()

#get the file name
filename = client.recv(1024).decode('utf-8')

#Recieve all of the data, both the ciphertext and the IV together
#This is formated as ciphertext....<IV>IV...<END>
done = False
all_data = b""
while not done:
    data = client.recv(1024)
    if all_data[-5:] == b"<END>":
        done = True
    else:
        all_data += data

#Use the ending tags to seperate the data
iv_start = all_data.find(b"<IV>")
iv_end = all_data.find(b"<END>")
ciphertext = all_data [:iv_start]
iv = all_data[iv_start + len(b"<IV>"):iv_end]

#decrypt
try:

    iv = b64decode(iv)
    ct = b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    file = open(filename, "wb")
    file.write(pt)
except (ValueError, KeyError):
    print("Incorrect decryption")

#close
file.close()
client.close()
server.close()