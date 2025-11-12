# Repurpose a Galaxy Tab 6 Keyboard with MicroPython
The Galaxy Tab 6 tablet can be used with a dedicated keyboard.
The keyboard connect the tablet through a Bluetooth connexion.
![Galaxy Tab 6 Keyboard](docs/Samsun-Galaxy-Tab-6-Keyboard.jpg)
Galaxy Tab 6 from 2019 is now a deprecated hardware (2025, OS no more maintained).

__I wanted to repurpose the keyboard for some MicroPython projects__.
Unfortunately the bluetooth keyboard (bt 3.5) could not be paired with other devices. So I open the keyboard and tried to workaround the Bluetooth connectivity.

# The keyboard connector
Inside the keyboard we do find a small board, a lipo and a kind of "matrix" for coding the keyboard.
![Inside Galaxy Tab 6 keyboard](docs/Samsung-Keyb-01.jpg)

![Main board inside Galaxy Tab 6 keyboard](docs/Samsung-Keyb-02.jpg)

Usually a keypad are organized in column/row matrix making easy to detect which key is pressed. Just actives the column one by one and read the columns to detect which key is pressed. 
![Usual Keypad](docs/keypad-example.jpg)

__Spoiler Alert__ : however, on the keyboard, some of the pins can act for both; the column and the row. It looks very strange but once understand, an appropriate read process can be applied.

Each keyboard lines is terminated by a 35 KΩ pull-down resistor except for line 1 to 5. So all lines & rows are tied to ground. Lines 1 to 5 
![Keyboard connector](docs/Keyboard-conn.png)
Some other lines (see the dots on the connector) are connected to an external chip labelled V5. 
Possibly a power line Mofset as this component is also used on a touchpad line. 

So I did expect that lines 6, 9,14,19,24 were row columns. The [tester1.py](examples/tester1.py) script demonstrated that I'm wrong. So I don't really know the behavior of such components and lines. 

# Hacking the keyboard matrix
By using 0.2mm varnished wire, it is possible to wire the connector outside of the keyboard. Using some hot-glue would be welcom to maintain the wires in place (and avoid them to break the solder joins).

![wiring the connector](docs/Samsung-Keyb-03.jpg)

![wiring the connector](docs/Samsung-Keyb-04.jpg)

Using a [CMS Prototyping board](https://shop.mchobby.be/product.php?id_product=864) (Olimex), the wires were reported on a 2.54mm alike breakout.

![connector breakout](docs/Samsung-Keyb-05.jpg)

Then a Pico with 2x [MCP23017 GPIO expander](https://shop.mchobby.be/product.php?id_product=218) was connected to the keyboard breakout.

![mcp2307 pinout](docs/mcp2307.jpg)

A particular attention was taken to connect the keyboard pins 1 to 26 in the same order than gpio expander. So, we have a direct mapping between the mcp23017 and the keyboard connector.

![Keyboard to mcp23017](docs/Keyboard-to-mcp.jpg)

Despite many tests, it was difficult to get consistant results. Then I made the assumption that keyboard pin 1 to 5 didn't have pull-down because they are connected directly to the MCU (and MCU offering the pull-down service).

So I __added 22 KΩ pull-down on keyboard pin 1 to 5__ (MCP #0 GPIO 0 to 4) then everything went quite better!

![Keyboard to mcp23017](docs/Keyboard-to-mcp-02.jpg)

# Decipher the keyboard matrix

The [tester2.py](examples/tester2.py) was used to decipher the matrix. The script use the keyboard connector pin identification (so from 1 to 26).

Press a KEY on a keyboard then starts the script.

At startup, the script first turns all the MCP23017 GPIOs as input with activated pull-up.

Then the script select a pin, switch it as output and set it HIGH (this is the __driver pin__). The script will then scan the remaining 25 input pins to detect a HIGH level. 

If a HIGH level is detected then we identified the __read pin__ for the keyboard key. The script prints the __driver pin__, __read pin__ combination on the  output.

When the read pass is complete, the __driver pin__ is switch back to input mode with pull-up. The script then jump to the next __driver pin__ and repeat the read process.

The data is collected into the [scan-result.ods](docs/scan-result.ods) spreadsheet.

![Scan Result excerp](docs/scan_result.jpg)

On the excerp here above, the F10 key is detected with the __driver pin__ 10 which activates the __read pin__ 15. 

The same __drive pin__ 10 is also used to detect the F9 key. This time, it will be on the __read pin__ 13.

Thanks to the [tester2-driver-pin-detect.py](examples/tester2-driver-pin-detect.py), all the drive pin and read pin have been identified.

* Driver pins : [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
* Read pins : [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

# Quick read
The [tester3.py](examples/tester3.py) script is an optimized version of the former [tester2.py](examples/tester2.py). 

That version only activates the known driver pins then reads 16 GPIOs in one single operation (2 bytes transfer over the I2C bus).