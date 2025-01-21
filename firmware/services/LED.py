from Service import Service
import machine, time

class LED(Service):
    led = machine.Pin('LED', machine.Pin.OUT)

    
    def flash(self, interval = 500):
        while True:
            time.sleep_ms(interval)
            self.log('Toggle')
            self.led.toggle()