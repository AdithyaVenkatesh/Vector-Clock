import socket
import threading
import socket
import time
import random

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
randtime = random.randint(10, 20)

client_data = {}


def clockTime(connector, address):
    while True:
        # receive clock time
        clock_time=0
        clock_time_string = connector.recv(1024).decode()
        clock_time = int(clock_time_string)
        clock_time_diff = randtime - clock_time
        print('clock Difference', randtime,clock_time,clock_time_diff)

        client_data[address] = {
            "clock_time": clock_time,
            "time_difference": clock_time_diff,
            "connector"	: connector
        }
        time.sleep(10)

def clientConnection():

    while True:
        client_server_connector, addr = server.accept()
        client_address = str(addr[0]) + ":" + str(addr[1])

        print(client_address + " got connected successfully")

        current_thread = threading.Thread(target = clockTime ,args = (client_server_connector ,client_address, ))
        current_thread.start()


# subroutine function used to fetch average clock difference
def getAverageClockDiff():

    current_client_data = client_data.copy()

    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())


    sum_of_clock_difference = sum(time_difference_list)

    print('sumof clock difference', sum_of_clock_difference)

    average_clock_difference = sum_of_clock_difference \
                               / (len(client_data ) +1)

    print('average', average_clock_difference)

    return average_clock_difference

def synchronizeAllClocks():

    while True:

        print("New synchronization cycle started.")
        print("Number of clients to be synchronized: " + \
              str(len(client_data)))

        if len(client_data) > 0:

            average_clock_difference = getAverageClockDiff()

            for client_addr, client in client_data.items():
                try:
                    synchronized_time = randtime + average_clock_difference

                    client['connector'].send(str(
                        synchronized_time).encode())

                except Exception as e:
                    print("Something went wrong while " + \
                          "sending synchronized time " + \
                          "through " + str(client_addr))

        else :
            print("No client data." + \
                  " Synchronization not applicable.")

        print("\n\n")

        time.sleep(5)

def server_process():

    print("Deamon created successfully\n")
    server.listen(10)
    print("Clock server started...\n")
    print("Starting to make connections...\n")
    master_thread = threading.Thread(target = clientConnection ,args = ())
    master_thread.start()

    print("Starting synchronization parallelly...\n")
    sync_thread = threading.Thread(target = synchronizeAllClocks ,args = ())
    sync_thread.start()


if __name__ == '__main__':

    print(randtime)
    server_process()
