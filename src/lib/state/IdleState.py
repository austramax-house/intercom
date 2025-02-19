from GenericState import GenericState
import time

class IdleState(GenericState):
    idling = False

    def start(self):
        super(IdleState, self).start()
        self.app.device.event('button.released', self.released)
        self.idle()


    def stop(self):
        super(IdleState, self).stop()
        self.app.device.event('button.released', None)


    def idle(self):
        self.idling = True
        
        while self.idling:
            self.app.device.evaluate()
            time.sleep_ms(100)
        
    
    def released(self, key):
        if self.app.mqtt.connected:
            self.app.mqtt.publish(f'{self.app.mqtt.clientId}/button{key}/press')