import App

class Service:
    def __init__(self, app: App.App):
        self.app = app


    def name(self):
        return self.__class__.__name__
    
        
    def log(self, message):
        name = self.name()
        self.app.log(message, name)


    def start(self):
        pass