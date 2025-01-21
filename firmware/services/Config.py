from Service import Service
import json

class Config(Service):
    filename = '/config.json'
    defaults = {}
    config = {}
    loaded = False


    def get(self, key = ''):
        custom = self.config
        default = self.defaults
        
        for step in str.split(key, '.'):
            if step:
                if type(custom) is dict:
                    custom = custom[step] if step in custom else None
                if type(default) is dict:
                    default = default[step] if step in default else None
        
        return custom if custom else default


    def load(self):
        self.defaults = {}
        self.config = {}
        self.loaded = False

        self.log('Loading defaults')
        defaults = self.app.filesystem.read(f'/stubs{self.filename}')
        self.defaults = json.loads(defaults)

        self.log('Loading custom config')
        if not self.app.filesystem.exists(self.filename):
            self.log('Creating empty custom config')
            self.app.filesystem.write(self.filename, '{}')
        else:
            config = self.app.filesystem.read(self.filename)
            self.config = json.loads(config)

        self.log('Loading finished')
        self.loaded = True

