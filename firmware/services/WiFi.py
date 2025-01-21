from Service import Service
import network, time


class WiFi(Service):
    configured = False
    
    attempts = 0
    connected = False
    connection = None

    ssid = None
    key = None


    def setup(self):
        self.log('Loading configuration')
        self.configured = False
        config = self.app.config.get('wifi')
        
        if not config:
            self.log('Missing configuration')
            return
        
        if not config['key']:
            self.log('Missing key')
            return

        if not config['ssid']:
            self.log('Missing SSID')
            return
        
        self.configured = True
        self.log('Loading finished')


    def connect(self):
        self.log(f'{'Attempting' if self.attempts is 0 else 'Retrying'} connection')
        
        if not self.configured:
            self.log('Not yet configured')
            return
        
        self.connection = network.WLAN(network.WLAN.IF_STA)
        self.connection.active(True)
        self.connection.connect(self.ssid, self.key)

        self.connected = self.connection.isconnected()
        if self.connected:
            self.attempts = 0
            self.log('Connected successfully')
            return

        if self.attempts < 5:
            self.log(f'Failed to connect ({self.attempts} attempts)')
            time.sleep_ms(500)
            self.connect()

        self.log('Max attempts exceeded')
        self.attempts = 0
        self.connected = False
        self.connection = None
