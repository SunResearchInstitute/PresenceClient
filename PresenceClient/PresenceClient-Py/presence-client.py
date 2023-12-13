import argparse
import json
import socket
import struct
import time
import re
import requests
import os
from pypresence import Presence
from dotenv import load_dotenv

load_dotenv() # load environment variables from .env file

switch_ip = os.getenv('IP') #gets the IP from the environment variable                          #
client_id = os.getenv('APPLICATION_ID') #gets the client ID from the environment variable       # Made them global variables so they can be used in the Title class
                                                                                                #
rpc = Presence(str(client_id))                                                                  # also rpc is here to clear and close it in the title class(if that deosn't work the script will restart lol)

TCP_PORT = 0xCAFE
PACKETMAGIC = 0xFFAADD23

parser = argparse.ArgumentParser()
parser.add_argument('--ignore-home-screen', dest='ignore_home_screen', action='store_true', help='Don\'t display the home screen. Defaults to false if missing this flag.')
parser.add_argument('--ignore-tinfoil', dest='ignore_tinfoil', action='store_true', help='Don\'t display the Tinfoil app. Defaults to false if missing this flag.')

questOverrides = None
switchOverrides = None

try: 
    questOverrides = json.loads(requests.get("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/QuestApplicationOverrides.json").text)
    switchOverrides = json.loads(requests.get("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/SwitchApplicationOverrides.json").text)
except:
    print('Failed to retrieve Override files')
    exit()

#Defines a title packet
class Title:
    def __init__(self, raw_data):
        if len(raw_data) != 628:    #checks if the data is the correct length
            rpc.clear() #clears the RPC
            rpc.close() #closes the RPC
            os.system('python3 presence-client.py --ignore-home-screen --ignore-tinfoil') #restarts the script(best way to reinitialize the title packet and kill the rpc (if the rpc command didn't do it)(i have no idea how to do it otherwise))
        unpacker = struct.Struct('2L612s')
        enc_data = unpacker.unpack(raw_data)
        self.magic = int(enc_data[0])
        if int(enc_data[1]) == 0:
            self.pid = int(enc_data[1])
            self.name = 'Home Menu'
        if int(enc_data[1]) == 0:
            self.pid = int(enc_data[1])
            self.name = 'Tinfoil'
        else:
            self.pid = int(enc_data[1])
            self.name = enc_data[2].decode('utf-8', 'ignore').split('\x00')[0]
        if int(enc_data[0]) == PACKETMAGIC:
            if self.name in questOverrides:
                if questOverrides[self.name]['CustomName'] != '':
                    self.name = questOverrides[self.name]['CustomName']
        else:
            if self.name in switchOverrides:
                if switchOverrides[self.name]['CustomName'] != '':
                    self.name = switchOverrides[self.name]['CustomName']

def main():
    consoleargs = parser.parse_args()
    if not checkIP(switch_ip):
        print('Invalid IP')
        exit()

    try:
        rpc.connect()
        rpc.clear()
    except:
        print('Unable to start RPC!')
    switch_server_address = (switch_ip, TCP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect(switch_server_address)
            print('Successfully connected to %s' % switch_ip + ':' + str(TCP_PORT))
            break
        except socket.error as e:
            print(f'Error connecting to {switch_ip}:{TCP_PORT}. Retrying in 1 minute.')
            time.sleep(60) #wait 1 minute before retrying
    lastProgramName = ''
    startTimer = 0
    while True:
        data = None
        try:
            data = sock.recv(628)
        except socket.error as e:
            print('Could not connect to Server! Retrying...')
            time.sleep(1)
            try:
                sock.connect(switch_server_address)
                print('Successfully reconnected to %s' % repr(switch_server_address))
            except socket.error as e:
                print(f'Error reconnecting to {repr(switch_server_address)}. Retrying...')
                time.sleep(1)
                continue
        title = Title(data)
        if not hasattr(title, 'magic'): 
            os.system('python3 presence-client.py --ignore-home-screen --ignore-tinfoil')
            continue
        title = Title(data)
        if title.magic == PACKETMAGIC:
            if lastProgramName != title.name:
                startTimer = int(time.time())
            if consoleargs.ignore_home_screen and title.name == 'Home Menu':
                rpc.clear()
            if consoleargs.ignore_tinfoil and title.name == 'Tinfoil':
                rpc.clear()
            else:
                smallimagetext = ''
                largeimagekey = ''
                details = ''
                largeimagetext = title.name
                if int(title.pid) != PACKETMAGIC:
                    smallimagetext = 'SwitchPresence-Rewritten'
                    if title.name not in switchOverrides:
                        largeimagekey = iconFromPid(title.pid)
                        details = 'Playing ' + str(title.name)
                    else:
                        orinfo = switchOverrides[title.name]
                        largeimagekey = orinfo['CustomKey'] or iconFromPid(title.pid)
                        details = orinfo['CustomPrefix'] or 'Playing'
                        details += ' ' + title.name
                else:
                    smallimagetext = 'QuestPresence'
                    if title.name not in questOverrides:
                        largeimagekey = title.name.lower().replace(' ', '')
                        details = 'Playing ' + title.name
                    else:
                        orinfo = questOverrides[title.name]
                        largeimagekey = orinfo['CustomKey'] or title.name.lower().replace(
                            ' ', '')
                        details = orinfo['CustomPrefix'] or 'Playing'
                        details += ' ' + title.name
                if not title.name:
                    title.name = ''
                lastProgramName = title.name
                rpc.update(details=details, start=startTimer, large_image=largeimagekey,
                        large_text=largeimagetext, small_text=smallimagetext)
            time.sleep(1)
        else:
            time.sleep(1)
            rpc.clear()
            rpc.close()
            sock.close()
            exit()

# uses regex to validate ip
def checkIP(ip):
    regex = r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    return re.search(regex, ip)

def iconFromPid(pid):
    return '0' + str(hex(int(pid))).split('0x')[1]

if __name__ == '__main__':
    main()