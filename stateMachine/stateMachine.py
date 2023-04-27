import findMiningArea

class StateMachine:

    def __init__(self, startingState) -> None:
        self.CURRENT_STATE = startingState
        self.states = {
            "FIND MINE": findMiningArea.FindMiningArea()
        }

    def process(self, tango, color_frame, depth_frame) -> None:

        state = self.states[self.CURRENT_STATE].process(self, tango,
            color_frame, depth_frame)

        if (state):
            self.changeState(state)

    def changeState(self, state):
        self.CURRENT_STATE = state
