# Running cross-platform with Python
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

[PresenceClient](https://github.com/Sun-Research-University/PresenceClient) can now be run in Python

# Requirements
Follow [setup](https://github.com/butforme/PresenceClient/blob/master/README.md) found here

Download and install the latest version of [Python for your platform](https://www.python.org/downloads/)
### Use pip to install requirements
```sh
pip install pypresence
```
# Usage
First clone the repository.
```sh
git clone https://github.com/Sun-Research-University/PresenceClient.git
```

Then navigatge into the [PresenceClient-Py](https://github.com/butforme/PresenceClient/tree/master/PresenceClient/PresenceClient-Py) directory with the following command.
```sh
cd PresenceClient/PresenceClient/PresenceClient-Py
```

You can then simply run with
```sh
python presence_client.py (arguments...)
```
### Arguments
`ip` The IP address of your device.

`client_id` The Client ID of your Discord Rich Presence applicationz

`--ignore-home-screen` Don't display the home screen

Run the help command with `-h` or `--help`

```sh
usage: presence-client.py [-h] [--ignore-home-screen] ip client_id

positional arguments:
  ip                    The IP address of your device
  client_id             The Client ID of your Discord Rich Presence application

optional arguments:
  -h, --help            show this help message and exit
  --ignore-home-screen  Dont display the home screen. Defaults to false if missing this flag.
```
