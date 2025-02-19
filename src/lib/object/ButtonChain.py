from machine import ADC, Pin
import time

class ButtonChain:
    def __init__(self, pressed = None, released = None):
        self.active = None
        self.buttons = {}
        self.min = 999999
        self.max = 0
        self.pressed = pressed
        self.released = released


    def assign(self, pin):
        self.pin = Pin(pin)
        self.adc = ADC(self.pin)


    def add(self, key, min, max):
        if self.min > min:
            self.min = min
        if self.max < max:
            self.max = max
        self.buttons[key] = (min, max)


    def remove(self, key):
        del self.buttons[key]


    def evaluate(self):
        current = self.active
        next = None

        # two readings for sanity
        value1 = self.adc.read_u16()
        time.sleep_ms(10)
        value2 = self.adc.read_u16()
        value = max(value1, value2)
        
        # determine if any are pressed
        if self.min <= value <= self.max:
            for key in self.buttons:
                bounds = self.buttons[key]

                if value >= bounds[0] and value < bounds[1]:
                    next = key

        # set the next active
        self.active = next

        # same as before, nothing pressed
        if not current and not next:
            return

        # same as before, same pressed
        elif current is next:
            return

        # something pressed
        elif not current and next:
            self.pressed(next) if self.pressed else None
            return

        # something released
        elif current and not next:
            self.released(current) if self.released else None
            return

        # something else pressed
        elif current and next and current != next:
            self.released(current) if self.released else None
            self.pressed(next) if self.pressed else None
            return
