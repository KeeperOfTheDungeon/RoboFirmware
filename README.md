# RoboFirmware
This is a project to implement a 9-bit USART Communication with the PIO of the Raspberry Pi Pico.

## Structure
In this project contained are test scripts, which were part of the developement, and the main script of this project **pio_usart.py**, which implements a 9-bit usart communication.

## Execution
The script can be executed with either the Thonny ide or Visual Studio Code with an add on installed as describe in [this documentation](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf).

For Visual Studio Code add on to work the python version installed on the computer must be 3.11 or newer.
### Linux settings
On linux systems the user has to be part of the dialout group.
To do this execute:

`sudo usermod -a -G dialout ` *username*

Where *username* refers to your username. Otherwise the ide can't connect with the usb device.
Alternativelly, but not recommended, the ide or code editor can be launched with root privileges.
