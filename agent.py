import random
from collections import deque
import heapq
import math
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

        already_visited = state in self.visited_states

        if percept["food_here"]:
            action = "Suck"

        elif percept["wall_ahead"]:

            if already_visited:
               action = "Right"
            else:
                action = "Left"

        else:

            if already_visited:
                action = "Left"
            else:
                action = "Right"

        self.visited_states.add(state)

        self.last_action = action

        return action


class SearchAgent:
    """Goal-Based Search Agent using BFS, DFS and UCS."""

    def __init__(self):
        self.plan = []
        self.active_algo = "BFS"

class SearchAgent:
    """Goal-Based Search Agent using BFS, DFS and UCS."""

    def __init__(self):
        self.plan = []
        self.active_algo = "BFS"

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    def get_neighbors(self, state, grid_size, walls):   
        x, y = state
        width, height = grid_size

        moves = [
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
            ("Left", (x - 1, y)),
            ("Right", (x + 1, y))
        ]

        neighbors = []

        for action, (nx, ny) in moves:
            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny) not in walls
            ):
                neighbors.append((action, (nx, ny)))

        return neighbors

    def bfs_search(self, start, goal, walls, grid_size):
        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            state, path = frontier.popleft()

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(
                state, grid_size, walls
            ):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append(
                        (next_state, path + [action])
                    )

        return []

    def dfs_search(self, start, goal, walls, grid_size):
        frontier = [(start, [])]
        reached = {start}

        while frontier:
            state, path = frontier.pop()

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(
                state, grid_size, walls
            ):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append(
                        (next_state, path + [action])
                    )

        return []

    def ucs_search(self, start, goal, walls, grid_size):
        frontier = [(0, start, [])]
        reached = {start: 0}

        while frontier:
            cost, state, path = heapq.heappop(frontier)

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(
                state, grid_size, walls
            ):
                new_cost = cost + 1

                if (
                    next_state not in reached
                    or new_cost < reached[next_state]
                ):
                    reached[next_state] = new_cost
                    heapq.heappush(
                        frontier,
                        (new_cost, next_state, path + [action])
                    )

        return []

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type='manhattan'
    ):
        frontier = []
        reached_states = set()

        if heuristic_type == 'euclidean':
            heuristic = self.euclidean_distance
        else:
            heuristic = self.manhattan_distance

        h_cost = heuristic(start_pos, goal_pos)
        f_cost = h_cost

        heapq.heappush(
            frontier,
            (f_cost, 0, start_pos, [])
        )

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(
                frontier
            )

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            for action, next_pos in self.get_neighbors(
                current_pos,
                grid_size,
                walls
            ):
                if next_pos not in reached_states:

                    new_g_cost = g_cost + 1
                    new_h_cost = heuristic(
                        next_pos,
                        goal_pos
                    )
                    new_f_cost = new_g_cost + new_h_cost

                    heapq.heappush(
                        frontier,
                        (
                            new_f_cost,
                            new_g_cost,
                            next_pos,
                            path_taken + [action]
                        )
                    )

        return []

    def sense_and_act(self, percept):
        if percept["food_here"]:
            return "Suck"

        if not self.plan:
            start = tuple(percept["agent_pos"])
            grid_size = percept["grid_size"]
            walls = set(percept["walls"])
            all_food = percept["all_food"]

            if not all_food:
                return "Right"

            goal = min(
                all_food,
                key=lambda food: abs(food[0] - start[0])
                + abs(food[1] - start[1])
            )

            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start, goal, walls, grid_size
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start, goal, walls, grid_size
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start, goal, walls, grid_size
                )

            elif self.active_algo == "AStar":
                self.plan = self.astar_search(
                    start,
                    goal,
                    walls,
                    grid_size,
                    heuristic_type="manhattan"
                )    

        if self.plan:
            return self.plan.pop(0)

        return "Right"

