import os
import socket

from Crypto.Cipher import AES

key = b"Thisisatestkey12"
nonce = b"Thisisatestkey11"


def send_file(file: str):
    cipher = AES.new(key, AES.MODE_EAX, nonce)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    while True:
        file_size = os.path.getsize(file)

    # Opens file, and reads the data
        with open(file, "rb") as f:
            data = f.read()

    # Encrypts the data from the file
        encrypted = cipher.encrypt(data)
        try:
            # Sends the encrypted data to specified address/port
            client.send(file.encode())
            client.send(str(file_size).encode())
            client.sendall(encrypted)
            client.send(b"<END>")
            print("File(s) Sent!")

            client.close()
        except Exception as e:
            print(e)
