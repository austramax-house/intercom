from enums import ButtonStatus
from machine import Pin, PWM
from object import ButtonChain, ButtonGroup
import Service
import json

notes = [
    49, # G1
    52, # G#1
    55, # A1
    58, # A#1
    62, # B1
    65, # C2
    69, # C#2
    73, # D2
    78, # D#2
    82, # E2
    87, # F2
    92, # F#2
    98, # G2
    104, # G#2
    110, # A2
    117, # A#2
    123, # B2
    131, # C3
    139, # C#3
    147, # D3
    156, # D#3
    165, # E3
    175, # F3
    185, # F#3
    196, # G3
    208, # G#3
    220, # A3
    233, # A#3
    247, # B3
    262, # C4
]


class Device(Service.Service):
    groups = []
    status = {}
    events = {
        'button.pressed': None,
        'button.released': None,
    }


    def setup(self):
        self.log('Setting up device')

        # setup buzzer
        self.buzzer = PWM(Pin(8))

        # single buttons group
        singlesGroup = ButtonGroup(pressed = self.pressed, released = self.released)
        singlesGroup.add(1, 2)
        singlesGroup.add(2, 28)
        singlesGroup.add(3, 3)
        singlesGroup.add(4, 22)
        singlesGroup.add(5, 6)
        singlesGroup.add(6, 21)
        singlesGroup.add(7, 7)
        singlesGroup.add(8, 20)
        singlesGroup.add(9, 9)
        singlesGroup.add(10, 19)
        singlesGroup.add(11, 10)
        singlesGroup.add(12, 18)
        singlesGroup.add(13, 12)
        singlesGroup.add(14, 17)
        singlesGroup.add(15, 13)
        singlesGroup.add(16, 16)
        self.groups.append(singlesGroup)

        # left-hand chain
        oddChain = ButtonChain(pressed = self.pressed, released = self.released)
        oddChain.assign(26)
        oddChain.add(17, 62000, 66000)
        oddChain.add(19, 58000, 62000)
        oddChain.add(21, 54000, 58000)
        oddChain.add(23, 50000, 54000)
        oddChain.add(25, 46000, 50000)
        oddChain.add(27, 42000, 46000)
        oddChain.add(29, 38000, 42000)
        self.groups.append(oddChain)

        # right-hand chain
        evenChain = ButtonChain(pressed = self.pressed, released = self.released)
        evenChain.assign(27)
        evenChain.add(18, 62000, 66000)
        evenChain.add(20, 58000, 62000)
        evenChain.add(22, 54000, 58000)
        evenChain.add(24, 50000, 54000)
        evenChain.add(26, 46000, 50000)
        evenChain.add(28, 42000, 46000)
        evenChain.add(30, 38000, 42000)
        self.groups.append(evenChain)

    
    def event(self, key, callback):
        self.events[key] = callback


    def discover(self):
        self.log('Discovering devices')

        mqtt = self.app.mqtt
        if not mqtt.client or not mqtt.connected:
            count = 0
            for group in self.groups:
                count += len(group.buttons)
            self.log(f'Skipping discovery of {count} buttons')
            return
        
        # device
        topic = f'homeassistant/device/{mqtt.clientId}/config'
        payload =  {
            'device': {
                'identifiers': mqtt.clientId,
                'name': mqtt.clientId,
                'model': 'Intercom',
                'manufacturer': 'Arrisar Labs',
            },
            'origin': {
                'name': mqtt.clientId
            },
            'components': {}
        }

        mqtt.publish(topic, json.dumps(payload), retain=True)
        self.log(f'Published device discovery')

        # buttons
        for button in self.groups:
            for key in button.buttons.keys():
                topic = f'homeassistant/sensor/{mqtt.clientId}_Button{key}/config'
                payload = {
                    'name': f'Button {key} - Pressed',
                    'state_topic': f'{mqtt.clientId}/button{key}/press',
                    'platform': 'sensor',
                    'device_class': 'timestamp',
                    'unique_id': f'{mqtt.clientId}_button{key}',
                    'value_template': '{{ now() }}',
                    'device': {
                        'identifiers': mqtt.clientId,
                        'name': mqtt.clientId,
                    }
                }

                mqtt.publish(topic, json.dumps(payload), retain=True)
                self.log(f'Published button {key} discovery')


    def evaluate(self):
        for group in self.groups:
            group.evaluate()
        
        first = None
        for key in self.status:
            if self.status[key] is ButtonStatus.ON:
                first = key
                break
        
        if first:
            self.buzzer.freq(notes[first - 1])
            self.buzzer.duty_u16(64000)
        else:
            self.buzzer.duty_u16(0)


    def pressed(self, key):
        self.log(f"Button {key} pressed!")
        self.status[key] = ButtonStatus.ON
        self.events['button.pressed'](key) if self.events['button.pressed'] else None


    def released(self, key):
        self.log(f"Button {key} released!")
        self.status[key] = ButtonStatus.OFF
        self.events['button.released'](key) if self.events['button.released'] else None