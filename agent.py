import random
# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)

class SimpleReflexAgent:
    """Simple Reflex Agent using Condition-Action Rules"""

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Suck"

        elif percept["wall_ahead"]:
            return "Left"

        else:
            return "Right"


class ModelBasedAgent:
    """Model-Based Agent with Internal Memory"""

    def __init__(self):
        self.visited_states = set()
        self.last_action = None

    def sense_and_act(self, percept):

        state = (
            percept["food_here"],
            percept["wall_ahead"]
        )

        self.visited_states.add(state)

        if percept["food_here"]:
            action = "Suck"

        elif percept["wall_ahead"]:

            if state in self.visited_states:
                action = "Left"
            else:
                action = "Right"

        else:
            action = "Right"

        self.last_action = action

        return action