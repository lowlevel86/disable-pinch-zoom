#!/bin/python3

# This script disables the pinch-zoom on an K400+ keyboard.
# The technique used takes advantage of the fact that the touchpad hardware
# on the K400+ keyboard sends a very quick left ctrl keypress event signal.
# This signal is identified by its duration and rejected.

import os
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller

# shell commands: set left ctrl (keycode 27) to "mode switch"
#os.system('setxkbmap -layout us')
os.system('xmodmap -e "clear control"')
os.system('xmodmap -e "keycode 37 = Mode_switch"') #mode switch key
os.system('xmodmap -e "keycode 105 = Control_R"')
os.system('xmodmap -e "add control = Control_R"')

# optional set the windows key to the middle mouse button
#os.system('xkbset m')
#os.system('xkbset exp =m')
#os.system('xmodmap -e "keycode 133 = Pointer_Button2"')


# the touchpad on the keyboard holds the
# left ctrl key for less than 0.02 seconds
delay_secs = 0.02 #change this value if necessary


kb = Controller()
ctrl_is_down = False

def on_releaseNB(key):
    global ctrl_is_down
    
    if key == keyboard.Key.alt_gr:
        ctrl_is_down = False

def on_press(key):
    global ctrl_is_down, delay_secs

    if key == keyboard.Key.alt_gr:
        ctrl_is_down = True
        time.sleep(delay_secs)
        
        if ctrl_is_down == True:
            kb.press(Key.ctrl_r)

def on_release(key):
    global ctrl_is_down
    if key == keyboard.Key.alt_gr:
        kb.release(Key.ctrl_r)
        ctrl_is_down = False
        
    # Exiting this way may not be necessary
    if key == keyboard.Key.esc: # press the "esc" key to exit
        return False # Stop listener

# non-blocking listener
listenerNB = keyboard.Listener(on_release=on_releaseNB)
listenerNB.start()

# blocking listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# shell commands: set left ctrl back to normal
os.system('xmodmap -e "keycode 37 = Control_L"')
os.system('xmodmap -e "add control = Control_L"')

