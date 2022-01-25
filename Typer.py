from pynput import keyboard
from time import sleep
controller = keyboard.Controller()

def delete(word,offset=0):
    global controller
    for i in range(len(word)+offset):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)

def type(word,next_key=' '):
    global controller
    controller.type(word)
    controller.type(next_key)

def delete_and_type(word,unicode,next_key=' ',offset=0):
    delete(word,offset)
    type(unicode,next_key)

def switch_program(delay=0.2):
    global controller
    controller.press(keyboard.Key.alt_l),controller.press(keyboard.Key.tab)
    controller.release(keyboard.Key.alt_l),controller.release(keyboard.Key.tab)
    sleep(delay)
