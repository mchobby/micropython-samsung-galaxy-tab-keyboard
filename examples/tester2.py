# === tester2.py ===
# Activate each of the 26 pins (one by one) and try to read which of the 
# 25 remaining pins gets activated by a Key-Press.
#
# This allow to identify couples of [driven_pin,activated_pin] for each 
# key on the Keyboard. Note that connection works the both ways, so a 
# connection [6,24] will also be reported as [24,6].
#
# ONLY the combination with the lower value at the first position will be
# retained.
#
# The results are then encoded within the scan-result.ods spreadsheet.
#
from machine import Pin, I2C
from mcp230xx import MCP23017
import time
i2c = I2C(1,  sda=Pin(6), scl=Pin(7) )

def pretty_bin8( value ):
 return ('%08s'% bin(value).replace('0b','')).replace(' ','0')

class KBReader2:
 def __init__(self):
  self.mcps = [ MCP23017( i2c, 0x20 ), MCP23017( i2c, 0x21 ) ]
  # Set all the pins in input mode 
  for mcp in self.mcps:
   for i in range(16):
    mcp.setup( i, Pin.IN )

 def decode_idx( self, idx ):
  # identify the mcp and its output corresponding to pin idx on the connector (1..26)
  idx = idx-1 # getting MCP index
  _mcp = self.mcps[1] if idx > 15 else self.mcps[0]
  _idx = idx if idx <= 15 else idx-16
  return _mcp,_idx

 def read( self ):
  # Activates the Rows and try to read. Return the first result
  for row_idx in range(26): # 0..25
    _idx = row_idx + 1 # 1..26
    _r = []
    _mcp,_pin = self.decode_idx( _idx )
    _mcp.setup( _pin, Pin.OUT )
    _mcp.output( _pin, True )
    time.sleep_ms(20)

    # read input pins
    try:
      for col_idx in range( 26 ):
        _col_idx = col_idx + 1
        if _col_idx == _idx:
          continue
        __mcp, __idx = self.decode_idx( _col_idx)
        _bit = __mcp.input( __idx )
        if _bit:
          if _col_idx==2: # Ignore pin 2
            continue
          _r.append( str(_col_idx) )
    finally:
      _mcp.output( _pin, False )
      _mcp.setup( _pin, Pin.IN )


    if len(_r)>0:
      print( "Drive %s => Result on %s" % (_idx, ", ".join(_r)) )
      print( "-"*60 )
      
  return False

   



#mcp0.setup( 0, Pin.OUT )
#mcp0.output( 0, True )


#mcp1.setup( 8, Pin.OUT )
#mcp1.output( 8, True )

bk = KBReader2()
while True:
  bk.read()
  time.sleep_ms(100)

