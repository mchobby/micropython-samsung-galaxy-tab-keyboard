# === tester1.py ===
# Try to read the keyboard key based on the possible row pins identified on
# connector Pin 6, Pin 9, Pin 14, Pin 19, Pin 24.
#
# This doesn't work!
#
from machine import Pin, I2C
from mcp230xx import MCP23017
import time
i2c = I2C(1,  sda=Pin(6), scl=Pin(7) )

def pretty_bin8( value ):
 return ('%08s'% bin(value).replace('0b','')).replace(' ','0')

class KBReader:
 def __init__(self):
  self.mcps = [ MCP23017( i2c, 0x20 ), MCP23017( i2c, 0x21 ) ]
  # Pins controling the rows. Tuple of (MCP,mcp_pin)
  self.rows = [ (self.mcps[0],5), (self.mcps[0],8), (self.mcps[0],13), (self.mcps[1],2), (self.mcps[1],7) ]
  # Set all the pins in input mode 
  for mcp in self.mcps:
   for i in range(16):
    mcp.setup( i, Pin.IN )

 def read( self ):
  # Activates the Rows and try to read. Return the first result
  for row_idx,mcp_pin in enumerate( self.rows ):
   # configure as output
   # print( mcp_pin )
   mcp,pin = mcp_pin
   if mcp!=None:
    mcp.setup( pin, Pin.OUT )
    mcp.output( pin, True )

   time.sleep_ms(20)
   for _mcp in self.mcps:
    # Read all GPIOs (low level call)
    _mcp.read_gpio()
   b0 = self.mcps[0].gpio[0] & 0b11000000 # Ignore pins 1 to 5 & 6 (row)
   b1 = self.mcps[0].gpio[1] & 0b11011110 # Ignore bits 0 (row) and 5 (row)
   b2 = self.mcps[1].gpio[0] & 0b01111011 # Ignore bits 2 (row) and 7 (row)
   b3 = self.mcps[1].gpio[1]
   # Read bits from left to rigth
   print( "\t%s = %s %s %s %s" % (row_idx, pretty_bin8(b3), pretty_bin8(b2), pretty_bin8(b1), pretty_bin8(b0) ))

   # reconfigure ROW as input
   if mcp!=None:
    mcp.output( pin, False )
    mcp.setup( pin, Pin.IN )


#mcp0.setup( 0, Pin.OUT )
#mcp0.output( 0, True )


#mcp1.setup( 8, Pin.OUT )
#mcp1.output( 8, True )

bk = KBReader()
while True:
  print( "-"*60 )
  bk.read()
  time.sleep(1)

