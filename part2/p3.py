import socket
import random
import threading
import time
import pickle

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
connected = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
randtime = random.randint(0, 9)


vectorclock = [0, 1, 0]



def send():
    global vectorclock

    while True:
        print("Before Sending Message : ", vectorclock[0:3])
        vectorclock.append(1)
        data = pickle.dumps(vectorclock)
        time.sleep(2)
        client.send(data)
        time.sleep(10)


def receive():
    global vectorclock
    while True:
        Synchronized_time = client.recv(2048)
        recvdata = pickle.loads(Synchronized_time)
        print("After Sending Message",recvdata)
        vectorclock = recvdata

def clientprocess():
    send_message = threading.Thread(target=send)
    send_message.start()

    receive_message = threading.Thread(target=receive)
    receive_message.start()


if __name__ == '__main__':

    clientprocess()
