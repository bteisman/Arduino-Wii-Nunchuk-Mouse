# Arduino-Wii-Nunchuk-Mouse

For Mac Users

Arduino Code based off of example online by Gabriel Bianconi

Python file created by Ben Teisman

To setup and use:
  1. Setup Arduino Board like picture ArduinoBoard.png (from https://makezine.com/projects/make-33/wii-nunchuk-mouse/)
  2. Download Arduino code editor and upload ArduinoNunchukBoard.ino to your Arduino
  3. Download pyserial. Command in terminal: sudo pip install pyserial. Make sure to download pip first (sudo easy_install pip)
  4. Check port of current Arduino. Can be done be looking at tools section of Arduino app, or by typing in: ls /dev/cu.* and find port that isn't the bluetooth port when arduino is plugged in (may need to unplug other usb products other than arduino).
  5. update port variable in python file (dashes in code to help find section)
  6. Change range of computer screen if necessary in python file (dashes in code to help find section)
  7. Locate where files were downloaded in terminal and type python nunchuk.py to get started
  8. Select sensitivity
  9. May be beneficial to change center of nunchuk based off individual nunchuk (dashes in code to help find section)
  
For any comments, bugs, or questions, contact me on my github page.
  
