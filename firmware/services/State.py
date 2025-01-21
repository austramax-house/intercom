from Service import Service
import App, states

class State(Service):
    def __init__(self, app: App.App):
        self.app = app
        self.current = None
        self.states = {
            'ERROR': states.ErrorState(app),
            'IDLE': states.IdleState(app),
            'ONBOARD': states.OnboardState(app),
            'STARTUP': states.StartupState(app),
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