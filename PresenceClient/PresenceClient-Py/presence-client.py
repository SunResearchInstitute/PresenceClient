import sys
import socket
import struct
import time
import re
from pypresence import Presence

TCP_PORT = 51966 #0xCAFE
PACKETMAGIC = 4289387811 #0xFFAADD23

def main():

    switch_ip = sys.argv[1]
    client_id = sys.argv[2]

    if(not checkIP(switch_ip)):
        print("Switch IP address is invalid...")
        abort()
    
    RPC = Presence(client_id)
    RPC.connect()
    RPC.clear()

    switch_server_address = (switch_ip, TCP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(switch_server_address)

    unpacker = struct.Struct('2L612s') # two unsigned longs and a char array of length 612

    """ while True: # Main listen loop
        print(RPC.update(state="TEST STATE", details="discord rpc wrapper for py"))
        time.sleep(15) #rich presence can only update every 15s """


#uses regex to validate ip address
def checkIP(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    return re.search(regex, ip)

def abort():
    print("Aborting...")
    exit()

if __name__ == '__main__':
    main()