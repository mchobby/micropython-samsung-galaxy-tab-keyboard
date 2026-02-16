# Samsung Galaxy Tab S6 Keyboard Interface
#
# The keyboard is interface through MCP23017 as described in the project.
#
# See https://github.com/mchobby/micropython-samsung-galaxy-tab-keyboard 
#
# After full keyboard testing, here are the detected driven pins and activated pins.
#   All driver pins : [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
#   All read   pins : [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
#
# Remarks:
# Even if pins 1 to 5 are not used in key detection they should be initialized
# in a given state to ensure stability.
#
from machine import Pin
from mcp230xx import MCP23017
from micropython import const
import time

KEY_ESC =const(333)
KEY_F1	=const(359)
KEY_F2	=const(328)
KEY_F3	=const(354)
KEY_F4	=const(406)
KEY_F5	=const(326)
KEY_F6	=const(352)
KEY_F7	=const(379)
KEY_F8	=const(246)
KEY_F9	=const(247)
KEY_F10	=const(249)
KEY_F11	=const(194)
KEY_F12	=const(195)
KEY_FINDER =const(337)
KEY_DUALSCREEN =const(168)
KEY_DEL        =const(169)

KEY_EXP =const(411)
KEY_1	=const(463)
KEY_2	=const(433)
KEY_3	=const(381)
KEY_4	=const(299)
KEY_5	=const(298)
KEY_6	=const(272)
KEY_7	=const(273)
KEY_8	=const(251)
KEY_9	=const(221)
KEY_0	=const(199)
KEY_PARENTHR =const(171)
KEY_MINUS =const(220) # - _
KEY_BACKSPACE =const(197)
KEY_TAB	=const(489)
KEY_RETURN  =const(175)
KEY_CAPSLOCK=const(468)
KEY_SHIFTL =const(338)
KEY_SHIFTR =const(364)
KEY_CTRL   =const(415)
KEY_FN     =const(544)
KEY_KEYB   =const(543) # Keyboard Key
KEY_ALT    =const(492)
KEY_LANG   =const(518)
KEY_ALTGR  =const(467)

KEY_A	=const(515)
KEY_Z	=const(434)
KEY_E	=const(382)
KEY_R	=const(303)
KEY_T	=const(301)
KEY_Y	=const(275)
KEY_U	=const(277)
KEY_I	=const(252)
KEY_O	=const(225)
KEY_P	=const(200)
KEY_Q	=const(541)
KEY_S	=const(435)
KEY_D	=const(384)
KEY_F	=const(305)
KEY_G	=const(304)
KEY_H	=const(278)
KEY_J	=const(279)
KEY_K	=const(253)
KEY_L	=const(227)
KEY_M	=const(201)
KEY_W	=const(568)
KEY_X	=const(436)
KEY_C	=const(383)
KEY_V	=const(308)
KEY_B	=const(306)
KEY_N	=const(280)
KEY_SPACE   =const(204)
KEY_DOLLARD =const(176)
KEY_CARRET  =const(223) # ^
KEY_PERCENT =const(226)
KEY_MU      =const(174)
KEY_LT	     =const(438) # Lower Than
KEY_COMA      =const(282)
KEY_SEMICOLON =const(254)
KEY_COLON     =const(228)
KEY_EQUAL     =const(202)

KEY_LEFT   =const(363)
KEY_UP     =const(178)
KEY_DOWN   =const(256)
KEY_RIGHT  =const(413)

# Keyboard definition dict with (default_key,shifted_key,altgr_key) 
KEYB_DEF = { KEY_A : ('a','A',None),
  KEY_Z	: ('z','Z',None),
  KEY_E	: ('e','E',None),
  KEY_R	: ('r','R',None),
  KEY_T : ('t','T',None),
  KEY_Y	: ('y','Y',None),
  KEY_U	: ('u','U',None),
  KEY_I	: ('i','I',None),
  KEY_O	: ('o','O',None),
  KEY_P	: ('p','P',None),
  KEY_Q	: ('q','Q',None),
  KEY_S	: ('s','S',None),
  KEY_D	: ('d','D',None),
  KEY_F	: ('f','F',None),
  KEY_G	: ('g','G',None),
  KEY_H	: ('h','H',None),
  KEY_J	: ('j','J',None),
  KEY_K	: ('k','K',None),
  KEY_L	: ('l','L',None),
  KEY_M	: ('m','M',None),
  KEY_W	: ('w','W',None),
  KEY_X	: ('x','X',None),
  KEY_C	: ('c','C',None),
  KEY_V	: ('v','V',None),
  KEY_B	: ('b','B',None),
  KEY_N	: ('n','N',None),
  KEY_1 : ('&','1','|'),
  KEY_2 : ('e','2','@'), # é
  KEY_3 : ('"','3','#'),
  KEY_4 : ("'",'4',None),
  KEY_5 : ('(','5',None),
  KEY_6 : (' ','6','^'),
  KEY_7 : ('e','7',None), # è
  KEY_8 : ('!','8',None),
  KEY_9 : ('c','9','{'), # ç
  KEY_0 : ('a','0','}'), # à
  KEY_SPACE    : (' ',' ',None),
  KEY_TAB      : ('\t','\t',None),
  KEY_PARENTHR : (')','°',None),  # )
  KEY_MINUS    : ('-','_',None),
  KEY_DOLLARD  : ('$','*',']'),
  KEY_CARRET   : ('^',' ','['),  # ^,",[
  KEY_PERCENT  : ('u','%',"'"),  # %,ù,'
  KEY_MU       : ('u',' ',"'"),  #µ,£,`
  KEY_LT       : ('<','>','\\'), #<,>,\
  KEY_COMA     : (',','?',None),
  KEY_SEMICOLON: (';','.',None),
  KEY_COLON    : (':','/',None),
  KEY_EQUAL    : ('=','+','~'),
  KEY_RETURN   : (chr(13),chr(10),None),
  KEY_TAB      : (chr(9) ,chr(9),None),
  KEY_BACKSPACE: (chr(8) ,chr(8),None),
  KEY_ESC      : (chr(27),chr(27),None)
 }

MODIFIERS = [ KEY_SHIFTL, KEY_SHIFTR, KEY_CTRL, KEY_FN, KEY_ALT, KEY_ALTGR ]


class SGTKeyb:
    """ Samsung Galaxy Tab S6 Keyboard Interface """
    def __init__(self, i2c, addr1, addr2):
        self.mcps = [ MCP23017(i2c, addr1), MCP23017(i2c, addr2) ]
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

        self._last_read_key = None   # last ASCII key readed by read_key
        self._last_read_start = None # Start time of the last readed key
        self.repeat_start = 1000     # Start repeating a char after 1000ms
        
        

    def decode_idx( self, idx ):
        # identify the mcp and its output corresponding to pin idx on the connector (1..26)
        idx = idx-1 # getting MCP index
        _mcp = self.mcps[1] if idx > 15 else self.mcps[0]
        _idx = idx if idx <= 15 else idx-16
        return _mcp,_idx

    def scan_matrix( self ):
        # Activates the Rows and try to read. Return list of KeyID
        # KeyID = driver_line * 26 + reader_line
        _r = []
        for drive_pin in self.drive_pins:
            # Activates a Driver Pin
            _mcp,_pin = self.decode_idx( drive_pin )
            _mcp.setup( _pin, Pin.OUT )
            _mcp.output( _pin, True )
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
                        num_value = (scan_value[0]*26)+scan_value[1]
                        if not(num_value in _r):
                            _r.append( num_value )
            finally:
                _mcp.output( _pin, False )
                _mcp.setup( _pin, Pin.IN )               
        return _r if len(_r)>0 else None 


    def scan_key( self ):
        """ Scan the matrix and returns (KeyID,ASCII,modifier_list). The list of modifiers may be [ShiftKey, ALT, etc]. 
            KeyID : may returns None when no key is detected.
            ASCII : corresponding ascii char when it applies (otherwise None)
            Notice that KeyID may be None if only modifier keys are pressed.  """
        _r = self.scan_matrix()
        if _r==None:
            return None
        _m = [] # Modifiers
        _key = None
        for key_id in _r:
            if key_id in MODIFIERS:
                _m.append( key_id )
            else:
                if _key == None:
                    _key = key_id
        _data = None # Key Definitionn data
        _a = None # Ascii representation
        if _key in KEYB_DEF:
            _data = KEYB_DEF[_key]
            if KEY_ALTGR in _m:
                _a = _data[2]
            elif (KEY_SHIFTR in _m) or (KEY_SHIFTL in _m):
                _a = _data[1]
            else:
                _a = _data[0]
        return ( key_id, _a, _m ) # key_id, ascii_repr, _modifier


    def read_key( self, timeout=None ):
        """ Scan the matrix and returns only characters that have entries in the 
            KEYB_DEF (includes Return, escape, tab, etc). May returns None in
            case of timeout (in ms) """
        start = time.ticks_ms()
        while True:
            if (timeout!=None) and (time.ticks_diff( time.ticks_ms(), start) > timeout):
                return None
            _r = self.scan_key() # key_id, _ascii, _modifier_list
            if (_r!=None) and (_r[1]!=None):
                if (self._last_read_key ==_r[1]) and (time.ticks_diff(time.ticks_ms(),self._last_read_start) <= self.repeat_start):
		    continue # Restart the loop
                if self._last_read_key != _r[1]:
                    self._last_read_key = _r[1]
                    self._last_read_start = time.ticks_ms()
                return _r[1]
        return None 

