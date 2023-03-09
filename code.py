# See general instructions at https://github.com/pimoroni/pmk-circuitpython
# Theis script is to build a macro pad for the Immersions VJ app on the iPad
# More info: https://bruchansky.name/immersionsvj/

from pmk import PMK, hsv_to_rgb
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware

import random
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up the keyboard
keybow = PMK(Hardware())
keys = keybow.keys
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Hue color for each key
colors = [170,170,170,50,
          170,240,240,50,
          100,100,100,50,
          360,300,300,20    
]

# Codes returned when keys are pressed once
keymap =    [0,
             0,
             0,
             Keycode.ONE,
             0,
             0,
             0,
             Keycode.TWO,
             Keycode.B,
             Keycode.V,
             Keycode.C,
             Keycode.THREE,
             Keycode.FIVE,
             0,
             0,
             Keycode.FOUR]

# Codes returned when keys are pressed continuously
keymapcont =    [Keycode.LEFT_ARROW,
             Keycode.DOWN_ARROW,
             Keycode.UP_ARROW,
             0,
             Keycode.RIGHT_ARROW,
             Keycode.COMMA,
             Keycode.PERIOD,
             0,
             0,
             0,
             0,
             0,
             0,
             Keycode.KEYPAD_MINUS,
             Keycode.KEYPAD_PLUS,
             0]

# Returns a number oscillating between 0 and 1
# frequency: number of steps to complete a full oscillation
# step: current step
def beat(step,frequency):
    localstep = step % frequency
    localstep2 = localstep % frequency/2
    if (localstep>=frequency/2 and localstep !=frequency):
        localstep2=frequency/2-localstep2
    v=localstep2*2/frequency
    return v

# Handle single key press
for key in keys:
    @keybow.on_press(key)
    def press_handler(key):
        keycode = keymap[key.number]
        if (keycode!=0):
            keyboard.send(keycode) # send code to the app once

step = 0 # to sync color animations
randomcolor = random.random() #random hue color assigned to upper right key

while True:
    keybow.update()

    # maximum animation cycle is 120 steps
    if step==120:
        step=0
    else:
        step=step+1
    
    for key in keys:
        # if a key is pressed, then make it brighter
        if key.pressed:
            s=1
            v=1
            if colors[key.number]==300: # exception to keep right-middle keys in white
                s=0
            if key.number == 15: # exception to keep random color of upper-right key 
                r, g, b = hsv_to_rgb(randomcolor,s,v)
            else: # make the key brighter
                r, g, b = hsv_to_rgb(colors[key.number]/360,s,v)
            key.set_led(r,g,b)
            keycode = keymapcont[key.number]
            if (keycode!=0):
                keyboard.send(keycode)   # send code continuously to the app
        # if no key is pressed, animate key colors
        else:
            s=1
            v=0.06
            h=colors[key.number]/360
            if colors[key.number]==300: # exception to display right-middle keys in white
                s=0
            if key.number == 10:
                v = beat(step,20)*0.06
            if key.number == 9:
                v = beat(step,60)*0.06
            if key.number == 3:
                v = 0.02+beat(step,30)*0.04
            if key.number == 7:
                v = 0.02+beat(step,60)*0.04
            if key.number == 11:
                v = 0.02+beat(step,120)*0.04
            if key.number == 15: # change random color of the upper-right key
                if step % 30 ==1:
                    randomcolor = random.random()
                h = randomcolor
                v = beat(step,30)*0.06
            if key.number == 12:
                v=0.08
            
            r, g, b = hsv_to_rgb(h,s,v)
            key.set_led(r,g,b)