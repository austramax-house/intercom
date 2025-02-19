import Service
import App, state

class State(Service.Service):
    def __init__(self, app: App.App):
        self.app = app
        self.current = None
        self.states = {
            'ERROR': state.ErrorState(app),
            'IDLE': state.IdleState(app),
            'ONBOARD': state.OnboardState(app),
            'STARTUP': state.StartupState(app),
        }

    def enter(self, state):
        self.current = state
        if self.current:
            self.states[self.current].start()

    def exit(self):
        if self.current:
            self.states[self.current].stop()

    def transition(self, state):
        self.exit()
        self.enter(state)