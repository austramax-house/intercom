from GenericState import GenericState

class StartupState(GenericState):
    def start(self):
        super(StartupState, self).start()
        self.setup()
    

    def setup(self):
        self.log('Setting up application')

        # filesystem
        self.app.filesystem.mount()
        if not self.app.filesystem.mounted:
            self.log('Unable to mount filesystem')
            self.app.state.transition('ERROR')
            return

        # config
        self.app.config.load()
        if not self.app.config.loaded:
            self.log('Unable to load config')
            self.app.state.transition('ERROR')
            return

        # wifi
        self.app.wifi.setup()
        if not self.app.wifi.configured:
            self.app.state.transition('ONBOARD')
            return
        
        self.app.wifi.connect()
        if not self.app.wifi.connected:
            self.app.state.transition('ONBOARD')
            return

        # mqtt
        pass

        # continue
        self.app.state.transition('IDLE')