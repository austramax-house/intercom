import App

class GenericState:
    def __init__(self, app: App.App):
        self.app = app


    def log(self, message):
        name = self.name()
        self.app.log(message, name)


    def name(self):
        return self.__class__.__name__


    def start(self):
        self.log('Entering state')
        
    
    def stop(self):
        self.log('Exiting state')