#!/usr/bin/python3
# coding=utf-8
# === tester3-groups.py ===
# grab the [driven_pin,activated_pin] combinatinn from the scan-result.ods 
# spreadsheet (stored as string).
#
# Group the read pins under each driver pins
# The scrit output is:
#   all driver pin
#   [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
#
#   All result pins
#   [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
#
from itertools import combinations
s = """12,21
13,21
12,16
13,16
15,16
12,14
13,14
14,15
10,12
10,13
10,15
7,12
7,13
12,25
6,12
6,13

15,21
17,21
16,17
14,17
11,13
11,12
9,12
9,13
10,17
8,13
7,17
6,15
8,12
7,15

18,21
19,21
16,18
14,18
11,17
11,15
9,15
9,17
10,18
8,17
7,18
8,15
6,20
6,19

17,26
20,21
16,19
14,20
11,19
11,18
9,18
9,19
10,19
8,19
7,19
8,18
6,18

12,26
16,22
21,22
16,20
14,19
11,22
11,20
9,20
9,22
10,20
8,20
7,20
13,26

15,25
20,24
20,23
18,24
7,22
19,24
17,25
13,25
6,22
10,22
15,23"""

def extract():
    global s
    _d = {}
    for line in s.split('\n'):
        if len(line)==0:
            continue
        driver_pin=int(line.split(',')[0])
        read_pin=int(line.split(',')[1])
        if not(driver_pin in _d):
            _d[driver_pin] = []
        _r = _d[driver_pin]
        if not(read_pin in _r):
            _r.append( read_pin )
    return _d

print( "all groups by driver_pin" )
d = extract()
print( d )

# Combines the drivers pins 2 by 2
drive_combinations = combinations( d.keys(), 2 )

# Try to detect if both driver pin can be used in the same time
# to detect key press
for driver1, driver2 in drive_combinations:
    # Same driver Pin ?
    if driver1==driver2:
        continue
    # Is the driver pin is a read pin in the other group
    if driver1 in d[driver2]:
        continue
    if driver2 in d[driver1]:
        continue
    if any( [ read2_pin in d[driver1] for read2_pin in d[driver2] ] ):
        continue
    print( "Both %i and %i drive pins can be used at the same time" % (driver1, driver2) )
    print( "\t %i reads %s" % (driver1,d[driver1]) )
    print( "\t %i reads %s" % (driver2,d[driver2]) )
    

