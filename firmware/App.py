from services import Bluetooth
from services import Config
from services import Filesystem
from services import Kernel
from services import LED
from services import MQTT
from services import State
from services import WiFi


class App:
    def __init__(self):
        print()
        print('  Austramax Intercom |')
        print('======================')


    def log(self, message, name = __name__):
        left = ' ' * (20 - len(name))
        print(f'{left}{name} | {message}')


    def setup(self):
        self.log('Setting up services')
        self.bluetooth = Bluetooth(self)
        self.config = Config(self)
        self.filesystem = Filesystem(self)
        self.kernel = Kernel(self)
        self.led = LED(self)
        self.mqtt = MQTT(self)
        self.state = State(self)
        self.wifi = WiFi(self)


    def start(self):
        self.log('Starting application')
        self.state.transition('STARTUP')
        print()
