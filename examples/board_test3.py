# === board_test3.py ===
# After full keyboard testing, here are the detected driven pins and activated pins.
#   All driver pins : [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
#   All read   pins : [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
#
# This script performs an optimized keyboard scanning to detects the key-press.
#
# Remarks:
# Even if pins 1 to 5 are not used in key detection they should be initialized
# in a given state to ensure stability.
#
from machine import Pin, I2C
from mcp230xx import MCP23017
import time
i2c = I2C(1,  sda=Pin(6), scl=Pin(7), freq=400_000 )

class KBReader3:
    def __init__(self):
        self.mcps = [ MCP23017( i2c, 0x24 ), MCP23017( i2c, 0x20 ) ]
        # define driver & read pins in range of 1..26
        self.drive_pins = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        self.read_pins  = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        # Set all the pins in input mode
        for _pin in list( set(self.drive_pins).union(self.read_pins) ):
            _mcp,_idx = self.decode_idx( _pin )
            _mcp.setup( _idx, Pin.IN )
            
        # No false key-down detected when they are configured as Pin.IN
        self.mcps[0].setup( 4, Pin.IN ) # In or OUT with HIGH or LOW change nothing
        self.mcps[0].setup( 3, Pin.IN ) # In or OUT with HIGH or LOW change nothing
        self.mcps[0].setup( 2, Pin.IN ) # In or OUT with HIGH or LOW change nothing
        self.mcps[0].setup( 0, Pin.IN ) # In or OUT with HIGH or LOW change nothing
        
        # Required! this place the pin High with a low current
        self.mcps[0].setup( 1, Pin.IN ) 
        
        

    def decode_idx( self, idx ):
        # identify the mcp and its output corresponding to pin idx on the connector (1..26)
        idx = idx-1 # getting MCP index
        _mcp = self.mcps[1] if idx > 15 else self.mcps[0]
        _idx = idx if idx <= 15 else idx-16
        return _mcp,_idx

    def scan( self ):
        # Activates the Rows and try to read. Return the first result
        _r = []
        for drive_pin in self.drive_pins:
            # Activates a Driver Pin
            _mcp,_pin = self.decode_idx( drive_pin )
            _mcp.setup( _pin, Pin.OUT )
            _mcp.output( _pin, True )
            #time.sleep_ms(1)
            try:
                # Force read from the MCPs
                [ _.read_gpio() for _ in self.mcps ]
                # Read the inputs
                for read_pin in self.read_pins:
                    if read_pin==drive_pin: # Do not read the drive pin
                        continue
                    #if drive_pin==19 and read_pin==21:
                    #    print( "CATCH" )
                    read_mcp, read_p = self.decode_idx(read_pin)                    
                    if read_mcp.input( read_p, read=False ): # Do not refresh
                        # Always lower value first
                        scan_value = (read_pin,drive_pin) if read_pin<drive_pin else (drive_pin,read_pin)
                        if not(scan_value in _r):
                            _r.append( scan_value )
            finally:
                _mcp.output( _pin, False )
                _mcp.setup( _pin, Pin.IN )               
        return _r if len(_r)>0 else None 
  


kb = KBReader3()
while True:
  _r = kb.scan()
  if _r != None:
      print( _r )
      

