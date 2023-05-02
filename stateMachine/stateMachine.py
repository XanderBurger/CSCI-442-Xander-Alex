from stateMachine.miningState import MiningState
from stateMachine.findMiningArea import FindMiningArea
from stateMachine.goToMine import GoToMine
from stateMachine.goToStart import GoToStart
from stateMachine.findStartingArea import FindStartingArea
from stateMachine.startingArea import StartingArea
from stateMachine.finish import Finish
from stateMachine.goToPerson import GoToPerson
from stateMachine.tester import Test

class StateMachine:
    def __init__(self, tango, startingState) -> None:
        self.tango = tango
        self.states = {
            "FIND MINE": FindMiningArea(),
            "MINING AREA": MiningState(),
            "GO TO MINE": GoToMine(),
            "FIND START": FindStartingArea(),
            "GO TO START": GoToStart(),
            "STARTING AREA": StartingArea(),
            "FINISH": Finish(),
            "GO TO PERSON": GoToPerson(),
            "TEST": Test()
        }
        self.currentState = self.states[startingState]


    def process(self, tango, color_frame, depth_frame) -> None:
        nextState = self.currentState.process(tango,color_frame, depth_frame)
        if (nextState):
            self.changeState(nextState)


    def changeState(self, nextState):
        self.currentState.exitState(self.tango)
        self.currentState = self.states[nextState]
        self.currentState.enterState(self.tango)
