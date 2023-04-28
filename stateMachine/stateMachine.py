from stateMachine import miningState
from stateMachine import findMiningArea

class StateMachine:

    def __init__(self, startingState) -> None:
        self.states = {
            "FIND MINE": findMiningArea.FindMiningArea(),
            "MINING AREA": miningState.MiningArea(),
        }
        self.currentState = self.states[startingState]


    def process(self, tango, color_frame, depth_frame) -> None:
        nextState = self.currentState.process(tango,color_frame, depth_frame)
        if (nextState):
            self.changeState(nextState)


    def changeState(self, nextState):
        self.currentState.exitState(self)
        self.currentState = self.states[nextState]
        self.currentState.enterState(self)
