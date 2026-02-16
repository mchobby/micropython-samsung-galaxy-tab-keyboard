#
# Hacking the Galaxy Tab Keyboard with with MCP23017 and MicroPython
#
# See https://github.com/mchobby/micropython-samsung-galaxy-tab-keyboard
#
from machine import Pin, I2C
from mcp230xx import MCP23017
import time
from sgtkeyb import *

# Raspberry-Pi Pico
i2c = I2C(1,  sda=Pin(6), scl=Pin(7), freq=400_000 )

# Create the Samsung Galaxy Tab keyboard
kb = SGTKeyb(i2c, 0x24, 0x20)
while True:
  _r = kb.scan_matrix()
  if _r != None:
      print( _r )
