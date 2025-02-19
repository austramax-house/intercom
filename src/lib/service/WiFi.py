import Service
import network, time

class WiFi(Service.Service):
    configured = False
    
    attempts = 0
    connected = False
    connection = None

    hostname = None
    key = None
    ssid = None


    def setup(self):
        self.log('Loading configuration')
        self.configured = False
        config = self.app.config.get('wifi')
        
        if not config:
            self.log('Missing configuration')
            return

        if 'hostname' not in config or not config['hostname']:
            self.log('Missing device name')
            return
        
        if 'key' not in config or not config['key']:
            self.log('Missing key')
            return

        if 'ssid' not in config or not config['ssid']:
            self.log('Missing SSID')
            return
        
        self.configured = True
        self.hostname = config['hostname']
        self.key = config['key']
        self.ssid = config['ssid']
        self.log('Loading finished')


    def connect(self):
        attempting = 'Attempting' if self.attempts is 0 else 'Retrying'
        attempts = f' ({self.attempts} attempts)' if self.attempts > 0 else ''
        self.log(f'{attempting} connection{attempts}')

        if self.connected:
            self.log('Already connected')
            return

        self.connected = False
        self.connection = None
        
        if not self.configured:
            self.log('Not yet configured')
            return
        
        network.hostname(self.hostname)
        self.connection = network.WLAN(network.WLAN.IF_STA)
        self.connection.active(False)
        self.connection.active(True)
        self.connection.connect(self.ssid, self.key)

        deadline = time.ticks_add(time.ticks_ms(), 2000)
        self.connected = self.connection.isconnected()

        while self.connection.status() >=0 and not self.connected and time.ticks_diff(deadline, time.ticks_ms()) > 0:
            self.connected = self.connection.isconnected()
            time.sleep_ms(100)

        if self.connected:
            self.attempts = 0
            self.log('Connected successfully')
            return
        
        if self.attempts < 5:
            self.log(f'Failed to connect ({self.connection.status()})')
            self.attempts += 1
            time.sleep_ms(1000)
            return self.connect()

        self.log('Max attempts exceeded')
        self.attempts = 0
        self.connected = False
        self.connection = None
