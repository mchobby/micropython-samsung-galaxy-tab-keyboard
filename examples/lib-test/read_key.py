#
# Hacking the Galaxy Tab Keyboard with with MCP23017 and MicroPython
#
# See https://github.com/mchobby/micropython-samsung-galaxy-tab-keyboard
#
from machine import Pin, I2C
from mcp230xx import MCP23017
import time, sys
from sgtkeyb import *

# Raspberry-Pi Pico
i2c = I2C(1,  sda=Pin(6), scl=Pin(7), freq=400_000 )

# Create the Samsung Galaxy Tab keyboard
kb = SGTKeyb(i2c, 0x24, 0x20)
while True:
  # Read ascii char from keyboard
  _c = kb.read_key() # timeout
  if _c != None:
      # print( _c )
      sys.stdout.write( _c )
