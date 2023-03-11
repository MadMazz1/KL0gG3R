import os
import socket
import sender

from Crypto.Cipher import AES

key = b"Thisisatestkey12"
nonce = b"Thisisatestkey11"

cipher = AES.new(key, AES.MODE_EAX, nonce)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))


def send_file(file: str):
    file_size = os.path.getsize(file)

    # Opens file, and reads the data
    with open(file, "rb") as f:
        data = f.read()

    # Encrypts the data from the file
    encrypted = cipher.encrypt(data)

    # Sends the encrypted data to specified address/port
    client.send(file.encode())
    client.send(str(file_size).encode())
    client.sendall(encrypted)
    client.send(b"<END>")
    print("File(s) Sent!")

    client.close()

send_file('file.txt')