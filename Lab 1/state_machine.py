import random
import math
from constants import *

class FiniteStateMachine(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        self.state.check_transition(agent, self)
        self.state.execute(agent)


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        self.time_ = 0
        # Todo: add initialization code

    def check_transition(self, agent, state_machine):
        if self.time_ > MOVE_FORWARD_TIME:
           state_machine.change_state(MoveInSpiralState())
        elif agent.get_bumper_state() == True:
            state_machine.change_state(GoBackState())
        # Todo: add logic to check and execute state transition
        pass

    def execute(self, agent):
        self.time_ += SAMPLE_TIME
        agent.set_velocity(FORWARD_SPEED, 0)
        # Todo: add execution logic
        pass


class MoveInSpiralState(State):
    def __init__(self):
        super().__init__("MoveInSpiral")
        self.time_ = 0
        # Todo: add initialization code
    
    def check_transition(self, agent, state_machine):
        if self.time_ > MOVE_IN_SPIRAL_TIME:
            state_machine.change_state(MoveForwardState())
        elif agent.get_bumper_state() == True:
            state_machine.change_state(GoBackState())
       # Todo: add logic to check and execute state transition
        pass

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED/(INITIAL_RADIUS_SPIRAL + SPIRAL_FACTOR*self.time_))
        self.time_ += SAMPLE_TIME
        # Todo: add execution logic
        pass


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        self.time_ = 0
        # Todo: add initialization code

    def check_transition(self, agent, state_machine):
        if self.time_ > GO_BACK_TIME:
            state_machine.change_state(RotateState())
        #Todo: add logic to check and execute state transition
        pass

    def execute(self, agent):
        self.time_ += SAMPLE_TIME
        agent.set_velocity(BACKWARD_SPEED, 0)
        # Todo: add execution logic
        pass


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        self.angle = (random.random()-0.5)*2*math.pi
        self.time_ = 0
        # Todo: add initialization code

    def check_transition(self, agent, state_machine):
        if ANGULAR_SPEED*self.time_ > self.angle:
            state_machine.change_state(MoveForwardState())
        #Todo: add logic to check and execute state transition
        pass
    
    def execute(self, agent):
        self.time_ += SAMPLE_TIME
        agent.set_velocity(0, ANGULAR_SPEED)
        # Todo: add execution logic
        pass