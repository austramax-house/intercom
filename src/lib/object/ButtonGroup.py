from enums import ButtonStatus
from machine import Pin
import time


class ButtonGroup:
    def __init__(self, pressed = None, released = None):
        self.buttons = {}
        self.pressed = pressed
        self.released = released


    def add(self, key, pin):
        self.buttons[key] = {
            'pin': Pin(pin, Pin.IN, Pin.PULL_UP),
            'status': ButtonStatus.OFF,
        }


    def remove(self, key):
        if key in self.buttons:
            del self.buttons


    def evaluate(self):
        current = {}
        initial = {}
        
        # get initial values
        for key in self.buttons:
            current[key] = self.buttons[key]['status']
            initial[key] = self.buttons[key]['pin'].value()

        # delay a second read to determine actual values
        time.sleep_ms(50)
        next = {}
        
        for key in self.buttons:
            next[key] = self.buttons[key]['pin'].value()

            # if values not the same, maintain for this loop
            if initial[key] is not next[key]:
                next[key] = current[key]
                continue


            # button is still not pressed
            if current[key] is ButtonStatus.OFF and next[key] is ButtonStatus.OFF:
                continue

            # button is still pressed
            if current[key] is ButtonStatus.ON and next[key] is ButtonStatus.ON:
                continue

            # button is being pressed
            if current[key] is ButtonStatus.OFF and next[key] is ButtonStatus.ON:
                self.buttons[key]['status'] = ButtonStatus.ON
                self.pressed(key) if self.pressed else None
                continue

            # button is being released
            if current[key] is ButtonStatus.ON and next[key] is ButtonStatus.OFF:
                self.buttons[key]['status'] = ButtonStatus.OFF
                self.released(key) if self.released else None
                continue