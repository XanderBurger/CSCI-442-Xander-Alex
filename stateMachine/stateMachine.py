from stateMachine.miningState import MiningState
from stateMachine.findMiningArea import FindMiningArea

class StateMachine:

    def __init__(self, startingState) -> None:
        self.states = {
            "FIND MINE": FindMiningArea(),
            "MINING AREA": MiningState(),
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
