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

    def process(self, centerOfGravity, center):

        if (self.CURRENT_STATE):
            self.CURRENT_STATE = self.states[self.CURRENT_STATE].process(
                centerOfGravity, center)
