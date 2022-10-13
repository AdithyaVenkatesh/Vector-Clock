import socket
import random
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
connected = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
randtime = random.randint(10, 20)


def send():
    while True:
        print(randtime)
        client.send(str(randtime).encode())
        print("Recent time sent successfully", end="\n\n")
        time.sleep(15)


def receive():

    while True:
        Synchronized_time = client.recv(1024).decode()
        print("Synchronized time at the client is: " + str(Synchronized_time), end="\n\n")


def clientprocess():
    send_message = threading.Thread(target=send)
    send_message.start()

    receive_message = threading.Thread(target=receive)
    receive_message.start()


if __name__ == '__main__':
    print(randtime)
    clientprocess()
