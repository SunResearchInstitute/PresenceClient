import sys
import socket
import struct
import time
import re
from pypresence import Presence

TCP_PORT = 51966 #0xCAFE
PACKETMAGIC = 4289387811 #0xFFAADD23

class Title:

    def __init__(self, raw_data):
        unpacker = struct.Struct('2L612s') # two unsigned longs and a char array of length 612
        enc_data = unpacker.unpack(raw_data)
        self.magic = enc_data[0]
        if enc_data[1] == 0:
            self.pid = '0x0100000000001000'
            self.name = 'Home Menu'
        else:
            self.pid = enc_data[1]
            self.name = enc_data[2].decode('utf-8','ignore').split('\x00')[0]


def main():

    switch_ip = sys.argv[1]
    client_id = sys.argv[2]

    if(not checkIP(switch_ip)):
        print("Error switch IP is invalid...")
        abort()
    
    RPC = Presence(client_id)
    RPC.connect()
    RPC.clear()

    switch_server_address = (switch_ip, TCP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock < 0:
        print("Error creating socket...")
        abort()
    
    try:
        sock.connect(switch_server_address)
        print("Successfully connected to %s" % repr(switch_server_address))
    except:
        print("Error connection to %s refused" % repr(switch_server_address))
        abort()

    data = sock.recv(628)


    """ while True: # Main listen loop
        print(RPC.update(state="TEST STATE", details="discord rpc wrapper for py"))
        time.sleep(15) #rich presence can only update every 15s """

def abort():
    print("Aborting...")
    exit()

#uses regex to validate ip
def checkIP(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    return re.search(regex, ip)

if __name__ == '__main__':
    main()