import socket
import threading
import rsa

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("8.8.8.8", 80))
#
# IP_tuple = sock.getsockname()
# (IP, PORT) = IP_tuple
#
# sock.close()
IP = ''
public_key, private_key = rsa.newkeys(2048)
public_partner = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, 7777))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(2048))
client.send(public_key.save_pkcs1("PEM"))


def send_message(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))


def receive_message(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(2048), private_key).decode())


threading.Thread(target=send_message, args=(client,)).start()
threading.Thread(target=receive_message, args=(client,)).start()
