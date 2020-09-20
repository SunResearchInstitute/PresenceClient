# Running with Python
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

# Requirements
Follow [setup](https://github.com/butforme/PresenceClient/blob/master/README.md) found here

Download and install the [latest version of Python](https://www.python.org/downloads/) for your platform
### Use pip to install requirements
Just run the following command
```sh
pip install pypresence
```
:warning: **If you plan on running this headlessly,** be aware for any rich presence application to work, the client must also be running an instance of the [Discord](https://discord.com/download) client.

# Usage
Download the latest ```presence-client.py``` file in the [Releases](https://github.com/Sun-Research-University/PresenceClient/releases) tab

Then just run the following command in the same directory as your ```presence-client.py``` file
```sh
python presence-client.py (arguments...)
```
### Arguments
`ip` The IP address of your device.

`client_id` The Client ID of your Discord Rich Presence application.

`--ignore-home-screen` Don't display the home screen.

Run the help command with `-h` or `--help`

```sh
usage: presence-client.py [-h] [--ignore-home-screen] ip client_id

positional arguments:
  ip                    The IP address of your device.
  client_id             The Client ID of your Discord Rich Presence application.

optional arguments:
  -h, --help            show this help message and exit
  --ignore-home-screen  Dont display the home screen. Defaults to false if missing this flag.
```
