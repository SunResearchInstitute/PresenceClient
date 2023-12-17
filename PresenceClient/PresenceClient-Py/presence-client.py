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
import subprocess

load_dotenv()

switch_ip = os.getenv('IP')
client_id = os.getenv('APPLICATION_ID') 

rpc = Presence(str(client_id))

TCP_PORT = 0xCAFE
PACKETMAGIC = 0xFFAADD23

parser = argparse.ArgumentParser()
parser.add_argument('--ignore-home-screen', dest='ignore_home_screen', action='store_true', help='Hide the home screen. Defaults to false if missing this flag.')
parser.add_argument('--ignore-tinfoil', dest='ignore_tinfoil', action='store_true', help='Hide the Tinfoil app. Defaults to false if missing this flag.')
consoleargs = parser.parse_args()

questOverrides = None
switchOverrides = None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
switch_server_address = (switch_ip, TCP_PORT)

try: 
    questOverrides = json.loads(requests.get("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/QuestApplicationOverrides.json").text)
    switchOverrides = json.loads(requests.get("https://raw.githubusercontent.com/Sun-Research-University/PresenceClient/master/Resource/SwitchApplicationOverrides.json").text)
except:
    print('Failed to retrieve Override files')
    exit()

def restart():
    rpc.clear()
    rpc.close()
    sock.close()

    command = ['python3', 'presence-client.py']

    if consoleargs.ignore_tinfoil:
        command.append('--ignore-tinfoil')
    if consoleargs.ignore_home_screen:
        command.append('--ignore-home-screen')

    subprocess.Popen(command)
    exit()


class Title:
    def __init__(self, raw_data):
        if len(raw_data) != 628:
            restart()

        unpacker = struct.Struct('2L612s')
        enc_data = unpacker.unpack(raw_data)

        self.magic = int(enc_data[0])
        self.pid = int(enc_data[1])

        if self.pid == 0:
            self.name = 'Home Menu' if self.magic != PACKETMAGIC else 'Tinfoil'
        else:
            self.name = enc_data[2].decode('utf-8', 'ignore').split('\x00')[0]

        overrides = questOverrides if self.magic == PACKETMAGIC else switchOverrides
        if overrides is not None and self.name in overrides and overrides[self.name]['CustomName']:
            self.name = overrides[self.name]['CustomName']

def main():
    if not checkIP(switch_ip):
        print('Invalid IP')
        exit()

    try:
        rpc.connect()
        rpc.clear()
    except:
        print('Unable to start RPC!')
    while True:
        try:
            sock.connect(switch_server_address)
            print(f'Successfully connected to {switch_ip}:{TCP_PORT}')
            break
        except socket.error:
            print(f'Error connecting to {switch_ip}:{TCP_PORT}. Retrying in 1 minute.')
            time.sleep(60)
    lastProgramName = ''
    startTimer = 0
    while True:
        data = None
        try:
            data = sock.recv(628)
        except socket.error:
            print('Could not connect to Server! Retrying...')
            time.sleep(60)
            try:
                sock.connect(switch_server_address)
                print('Successfully reconnected to %s' % repr(switch_server_address))
            except socket.error:
                print(f'Error reconnecting to {repr(switch_server_address)}. Retrying...')
                time.sleep(60)
                continue
        def get_details(title, overrides):
            if title.name in overrides:
                orinfo = overrides[title.name]
                largeimagekey = orinfo['CustomKey'] or iconFromPid(title.pid)
                details = orinfo['CustomPrefix'] or 'Playing'
            else:
                largeimagekey = iconFromPid(title.pid) if int(title.pid) != PACKETMAGIC else title.name.lower().replace(' ', '')
                details = 'Playing'
            details += ' ' + title.name
            return largeimagekey, details

        title = Title(data)
        if not hasattr(title, 'magic'): 
            restart()
            continue

        if title.magic == PACKETMAGIC:
            if lastProgramName != title.name:
                startTimer = int(time.time())
            if consoleargs.ignore_home_screen and title.name == 'Home Menu':
                rpc.clear()
            elif consoleargs.ignore_tinfoil and title.name == 'Tinfoil':
                rpc.clear()
            else:
                smallimagetext = 'SwitchPresence-Rewritten' if int(title.pid) != PACKETMAGIC else 'QuestPresence'
                overrides = switchOverrides if int(title.pid) != PACKETMAGIC else questOverrides
                largeimagekey, details = get_details(title, overrides)
                largeimagetext = title.name or ''
                lastProgramName = title.name or ''
                rpc.update(details=details, start=startTimer, large_image=largeimagekey,
                        large_text=largeimagetext, small_text=smallimagetext)
            time.sleep(1)
        else:
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