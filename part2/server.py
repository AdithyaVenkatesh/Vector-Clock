import socket
import threading
import socket
import time
import pickle

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

vectorclock = [1, 0, 0]
processvalue =[]
client_data = {}


def clockTime(connector, address):
    while True:
        # receive clock time
        global processvalue,vectorclock
        clock_time_string = connector.recv(2048)
        processvalue = pickle.loads(clock_time_string)
        print(processvalue)
        whichclient = processvalue[3]
        # print(whichclient)
        vectorclock[whichclient] = max(processvalue[whichclient], vectorclock[whichclient])
        vectorclock[whichclient] = vectorclock[whichclient] + 1
        print(vectorclock)
        senddata= pickle.dumps(vectorclock)
        connector.send(senddata)



def clientConnection():
    while True:
        client_server_connector, addr = server.accept()
        client_address = str(addr[0]) + ":" + str(addr[1])

        print(client_address + " got connected successfully")

        current_thread = threading.Thread(target=clockTime, args=(client_server_connector, client_address,))
        current_thread.start()


# subroutine function used to fetch average clock difference




def server_process():
    print("Deamon created successfully\n")
    server.listen(10)
    print("Clock server started...\n")
    print("Starting to make connections...\n")
    master_thread = threading.Thread(target=clientConnection, args=())
    master_thread.start()

    # print("Starting synchronization parallelly...\n")
    # sync_thread = threading.Thread(target = synchronizeAllClocks,args = ())
    # sync_thread.start()


if __name__ == '__main__':

    server_process()