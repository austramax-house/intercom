from service.Bluetooth import Bluetooth
from service.Config import Config
from service.Device import Device
from service.Filesystem import Filesystem
from service.Kernel import Kernel
from service.LED import LED
from service.MQTT import MQTT
from service.State import State
from service.WiFi import WiFi


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
        self.device = Device(self)
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
