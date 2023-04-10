from state import State


class Stop(State):
    def process(self, centerOfGravity, center):
        nextState = None
        print("STOP")
        return nextState
