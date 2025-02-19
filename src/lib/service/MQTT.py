import Service
import time
import umqtt.simple

class MQTT(Service.Service):
    configured = False
    
    attempts = 0
    connected = False
    client = None

    clientId = None
    server = None
    port = None
    username = None
    password = None


    def setup(self):
        self.log('Loading config')
        self.configured = False
        config = self.app.config.get('mqtt')
        
        if not config:
            self.log('Missing configuration')
            return
        
        if 'clientId' not in config or not config['clientId']:
            self.log('Missing client ID')
            return
        
        if 'server' not in config or not config['server']:
            self.log('Missing server')
            return
        
        if 'port' not in config or not config['port']:
            self.log('Missing port')
            return
        
        if 'username' not in config or not config['username']:
            self.log('Missing username')
            return

        if 'username' not in config or not config['username']:
            self.log('Missing username')
            return
        
        self.configured = True
        self.clientId = config['clientId']
        self.server = config['server']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        
        self.log('Config loaded')
        self.create()


    def create(self):
        self.log('Creating client')
        if not self.configured:
            self.log('Not yet configured')
            return
        
        port = self.port if self.port else 0
        self.client = umqtt.simple.MQTTClient(self.clientId, self.server, port, self.username, self.password)


    def connect(self):
        self.log('Connecting to MQTT broker')
        if not self.client:
            self.log('No client created')
            return
        
        if self.connected:
            self.log('Already connected')
            return
        
        try:
            time.sleep_ms(1000)
            self.client.connect(timeout=5)
        except: 
            self.connected = False
            self.log('Failed to connect')
            return

        self.connected = True


    def publish(self, topic, message = '', retain = True):
        if not self.connected or not self.client:
            self.log('Not connected')
            return
        
        self.client.publish(topic, message, retain)
        self.log(f'Published message to {topic}')