# Running cross-platform with Python
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
PresenceClient can now be run in Python
# Requirements
Follow [setup](https://github.com/butforme/PresenceClient/blob/master/README.md) found here
Download and install the latest version of [Python for your platform](https://www.python.org/downloads/)
### Use pip to install requirements
```sh
pip install pypresence
```
# Usage
You can run PresenceClient by executing the following command the [PresenceClient-Py](https://github.com/butforme/PresenceClient/tree/master/PresenceClient/PresenceClient-Py) folder
```sh
python presence_client.py
```
### Arguments
**ip**
The IP address of your device
**client_id**
The Client ID of your Discord Rich Presence application

Run the help command by adding flag ```-h```


```sh
usage: presence-client.py [-h] [--ignore-home-screen IGNORE_HOME_SCREEN] ip client_id

positional arguments:
  ip                    The IP address of your device
  client_id             The Client ID of your Discord Rich Presence application

optional arguments:
  -h, --help            show this help message and exit
  --ignore-home-screen IGNORE_HOME_SCREEN
                        Dont display the home screen
```
