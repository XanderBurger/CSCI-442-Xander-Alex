from stateForward import Forward
from stateStop import Stop
from stateLeft import Left
from stateRight import Right


class StateMachine:

    def __init__(self) -> None:
        self.CURRENT_STATE = "STOP"
        self.states = {
            "FORWARD": Forward(),
            "STOP": Stop(),
            "LEFT": Left(),
            "RIGHT": Right()
        }

    def process(self, centerOfGravity: float, center: tuple) -> None:

        state = self.states[self.CURRENT_STATE].process(
            centerOfGravity, center)

        if (state):
            self.changeState(state)

    def changeState(self, state):
        self.CURRENT_STATE = state
