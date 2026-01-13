# Trinket IO demo
# Welcome to CircuitPython :)

from touchio import *
from digitalio import *
from analogio import *
from board import *
import time
import neopixel
import random

# Capacitive touch on D3
touch = TouchIn(D1)

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 11
MAXLITBLINKPIXELS = 10
CURLITBLINKPIXELS = 0
LED_STATES = [0] * NUMPIXELS
neopixels = neopixel.NeoPixel(D3, NUMPIXELS, brightness=.8, auto_write=True)
DIRECTION = 1 # 1 == "up"
COLOR = 1 # 1 == "red"

# COLORS
RED = (255, 0, 0)
ORANGE = (255,165,0)
WHITE = (125, 125, 125)
BLUE = (0,0,255)
PURPLE = (180, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PINK = (200, 150, 160)
BLACK = (0, 0, 0)

COLORPALLET = [CYAN, BLUE, PURPLE, GREEN, PINK]
## COLORPALLET = [WHITE, WHITE, WHITE, WHITE]

######################### HELPERS ##############################

# Helper to convert analog input to voltage
# def getVoltage(pin):
#     return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def flicker(idx, rgbVal):
    neopixels.brightness = 1
    neopixels[idx] = rgbVal
    if idx > 2 and idx < NUMPIXELS -2:
        neopixels[idx -2] = rgbVal
        neopixels[idx -1] = rgbVal
    time.sleep(0.0125)
    neopixels[idx] = (0, 0, 0)
    neopixels.brightness = .1

def rainbowPulse(i):
    for p in range(NUMPIXELS):
        idx = int ((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)

def redPulse():
    aPixel = neopixels[0]
    rCur = aPixel[0]
    gCur = aPixel[1]
    bCur = aPixel[2]

    if DIRECTION == 1:
        neopixels.fill((rCur + 10, gCur, bCur))

    if DIRECTION == 2:
        neopixels.fill((rCur - 10, gCur, bCur))

def whitePulse():
    aPixel = neopixels[0]
    rCur = aPixel[0]
    gCur = aPixel[1]
    bCur = aPixel[2]

    if DIRECTION == 1:
        neopixels.fill((rCur + 10, gCur + 10, bCur + 10))

    if DIRECTION == 2:
        neopixels.fill((rCur - 10, gCur - 10, bCur - 10))

def blinkFade(blinkColor):
    # Count how many LEDs are currently on or fading
    currentLitPixels = sum(1 for state in LED_STATES if state > 0)

    # print("blinking")
    # currentLitPixels = 0
    # count total lit pixels
    for p in range(NUMPIXELS):
        aPixel = neopixels[p]
        # If a pixel is already lit, skip.
        if (aPixel[0] > 10 or aPixel[1] > 10 or aPixel[2] > 10):
            rCur = aPixel[0]
            gCur = aPixel[1]
            bCur = aPixel[2]

            if rCur <= 10:
                rCur = 10
            if gCur <= 10:
                gCur = 10
            if bCur <= 10:
                bCur = 10

            neopixels[p] = ((rCur - 10, gCur - 10, bCur - 10))
            currentLitPixels += 1

        if (aPixel[0] < 10 and aPixel[1] < 10 and aPixel[2] < 10):
            neopixels[p] = ((0,0,0))
            LED_STATES[p] = 0
            currentLitPixels -= 1
            ## time.sleep(.0125)

    # This is the pattern I've been trying to figure out for a while now. 
    if currentLitPixels < MAXLITBLINKPIXELS and random.randint(0,10) <= 6:
        # Find a pixel that isn't lit
        bDone=False
        while not bDone:
            randoPixel = random.randint(0,NUMPIXELS-1)
            aPixel = neopixels[randoPixel]

            if (aPixel[0] == 0):
                neopixels[randoPixel] = blinkColor
                LED_STATES[randoPixel] = 1
                currentLitPixels += 1
                ## time.sleep(.125)
                time.sleep((random.randint(0,10)/60))
                bDone=True


######################### MAIN LOOP ##############################

i = 0;
colorChange = 0;

while True:

    if touch.value:
        neopixels.fill(BLACK)
        flicker(random.randint(0, NUMPIXELS-1), WHITE)
        time.sleep(.1)
        colorChange = 1
        print("D1 touched!")
    else:
        if colorChange == 1:
            # print ("Color is changing!")
            if COLOR == 1:
                COLOR = 2
            if COLOR == 2:
                COLOR = 1

            colorChange = 0
        
        if COLOR == 1:
            blinkFade(WHITE)
            ## blinkFade(COLORPALLET[random.randint(0,4)])
            time.sleep(0.0312)
        if COLOR == 2:
            ## blinkFade(WHITE)
            blinkFade(COLORPALLET[random.randint(0,4)])
        if COLOR == 3:
            whitePulse()
        if COLOR == 4:
            i = (i+30) % 256  # run from 0 to 255
            neopixels.brightness = .5
            rainbowPulse(i)
        
        