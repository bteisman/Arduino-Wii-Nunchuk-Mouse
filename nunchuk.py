# Nunchuk.py
# A Wii Nunchuk converted into a computer mouse

# Created by Ben Teisman 2016

# Import the required libraries for this script
from Quartz.CoreGraphics import *
import sys, string, time, serial

#-----------------FOR MOVING MOUSE----------------------------------------------------------
def mouseEvent(type, posx, posy):
    if type == kCGEventRightMouseDown or type == kCGEventRightMouseUp:
        event = CGEventCreateMouseEvent(None,type,(posx,posy),kCGMouseButtonRight)
    else:
        event = CGEventCreateMouseEvent(None,type,(posx,posy),kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event)

def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy)

def mouseclick(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy)
    mouseEvent(kCGEventLeftMouseUp, posx,posy)

def mouseclickright(posx, posy):
    mouseEvent(kCGEventRightMouseDown, posx,posy)
    mouseEvent(kCGEventRightMouseUp, posx,posy)

def scroll_up():
    event = CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 1, -1)
    CGEventPost(kCGHIDEventTap, event)

def scroll_down():
    event = CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 1, 1)
    CGEventPost(kCGHIDEventTap, event)

# To keep track of mouse position
class mouse:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y

#---------------------------------------------------------------------------------------------

print "Wii Nunchuk Mouse"
print ""
print "Initializing..."
print ""
try:
    sensitivity = input("Sensitivity(1-5): ")
except:
    sensitivity = 1
if sensitivity != 1 and sensitivity != 2 and sensitivity != 3 and sensitivity != 4 and sensitivity != 5:
    sensitivity = 1
print ""
print "- If error occurs, please restart"
print "- Setup Arduino Board with Nunchuk program before running"
print "- Port and dimension are subject to change, see source code"
print "- Find port number in Tools section of Arduino"
print "- If program is non-responsive, check Arduino/port then serial inputs in code"
print ""
print "Mouse Movement = Analog Stick"
print "Left Click = zButton"
print "Right Click = cButton"
print "Scrolling = Both zButton and cButton and tilt up or down"
print ""
print "Waiting..."

current = mouse(640, 400)
mousemove(current.posx, current.posy)
mouseup = False
rightup = False
scroll = False

# The port to which your Arduino board is connected, make sure Arduino program is set up first----------------------------------------------------------------------------------------------
port = '/dev/cu.usbmodem1411'

# The baudrate of the Arduino program
baudrate = 19200

# Accelerometer Y
midAccelY = 510 

# Connect to the serial port
ser = serial.Serial(port, baudrate, timeout = 1)

# Wait 3s for things to stabilize
time.sleep(3)

# center of nunchuck ------------------------------------------------------------------------------------------------------------------------------------------------------
midX = 121
midY = 127

print ""
print "Ready!"
print ""
print "To quit press control and C at the same time"

# While the serial port is open
while ser.isOpen():

    # Read one line
    try:
        line = ser.readline()
    except:
        break

    # Strip the ending (\r\n)
    line = string.strip(line, '\r\n')

    # If it is not reading yet
    if line == '':
        continue

    # Split the string into an array containing the data from the Wii Nunchuk
    line = string.split(line, ' ')

    # If it is not reading yet
    if len(line) != 7:
        continue

    # Set variables for each of the values
    try:
        analogX = int(line[0])
        analogY = int(line[1])
        accelX = int(line[2])
        accelY = int(line[3])
        accelZ = int(line[4])
        zButton = int(line[5])
        cButton = int(line[6])
    except:
        continue

    # Scrolling the mouse. Doesn't move mouse
    if zButton == 1 and cButton == 1:
        scroll = True
        if (accelY - midAccelY > 0):
            scroll_up()
        else:
            scroll_down()

    else:
        # Click mouse on zButton up
        if zButton == 1 and cButton == 0 and not scroll:
            mouseup = True
        if mouseup and zButton == 0:
            mouseup = False
            mouseclick(current.posx, current.posy)  

        # Click mouse on zButton up
        if cButton == 1 and zButton == 0 and not scroll:
            rightup = True
        if rightup and cButton == 0:
            rightup = False
            mouseclickright(current.posx, current.posy)

        if scroll:
            scroll = False

        # Mouve mouse based on stick
        current.posx += sensitivity * ((analogX - midX) / 10)
        current.posy += -sensitivity * ((analogY - midY) / 10)
        # Range of computer screen ---------------------------------------------------------------------------------------------------------
        if current.posx < 0:
            current.posx = 0
        elif current.posx > 1280:
            current.posx = 1280
        if current.posy < 0:
            current.posy = 0
        elif current.posy > 800:
            current.posy = 800

        mousemove(current.posx, current.posy)
    

# After the program is over, close the serial port connection
ser.close()