import numpy as np
from time import time

class Node:
    def __init__(self, parent, state, pcost, hcost, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.pcost = pcost
        self.hcost = hcost
        self.cost = pcost + hcost

    def __hash__(self):
        return hash(str(self.state.flatten()))

    def __str__(self):
        return str(self.state)

    def __eq__(self, other):
        return hash(''.join(self.state.flatten())) == hash(''.join(other.state.flatten()))

    def __ne__(self, other):
        return hash(''.join(self.state.flatten())) != hash(''.join(other.state.flatten()))


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.hashes = {}

    def push(self, node):
        if hash(node) not in self.hashes:
            self.hashes[hash(node)] = 1
            self.queue.append(node)

    def pop(self):
        next_state = None
        state_cost = 10**18
        index = -1

        for i in range(len(self.queue)):
            if self.queue[i].cost < state_cost:
                state_cost = self.queue[i].cost
                next_state = self.queue[i]
                index = i

        if next_state:
            self.queue.pop(index)
            del self.hashes[hash(next_state)]
        return next_state

    def is_empty(self):
        return len(self.queue) == 0


class Environment:
    def __init__(self, start_state=None, goal_state=None):
        self.actions = [1, 2, 3, 4]  # 1-Up, 2-Down, 3-Right, 4-Left
        self.goal_state = goal_state or self.generate_goal_state()
        self.start_state = start_state or self.generate_start_state()

    def generate_start_state(self):
        start = np.zeros((7, 7))
        x = (0, 1, 5, 6)
        y = (0, 1, 5, 6)
        for i in x:
            for j in y:
                start[i][j] = -1
        x = (2, 3, 4)
        y = range(7)
        for i in x:
            for j in y:
                start[i][j] = 1
                start[j][i] = 1
        start[3][3] = 0
        return start

    def generate_goal_state(self):
        goal = np.zeros((7, 7))
        x = (0, 1, 5, 6)
        y = (0, 1, 5, 6)
        for i in x:
            for j in y:
                goal[i][j] = -1
        x = (2, 3, 4)
        y = range(7)
        for i in x:
            for j in y:
                goal[i][j] = 0
                goal[j][i] = 0
        goal[3][3] = 1
        return goal

    def get_start_state(self):
        return self.start_state

    def get_goal_state(self):
        return self.goal_state

    def get_next_states(self, state):
        new_states = []
        spaces = [(i, j) for i in range(7) for j in range(7) if state[i][j] == 0]

        for space in spaces:
            x, y = space
            if x > 1 and state[x-1][y] == 1 and state[x-2][y] == 1:
                new_state = state.copy()
                new_state[x][y] = 1
                new_state[x-2][y] = 0
                new_state[x-1][y] = 0
                action = f'({x-2}, {y}) -> ({x}, {y})'
                new_states.append((new_state, action))
            if x < 5 and state[x+1][y] == 1 and state[x+2][y] == 1:
                new_state = state.copy()
                new_state[x][y] = 1
                new_state[x+2][y] = 0
                new_state[x+1][y] = 0
                action = f'({x+2}, {y}) -> ({x}, {y})'
                new_states.append((new_state, action))
            if y > 1 and state[x][y-1] == 1 and state[x][y-2] == 1:
                new_state = state.copy()
                new_state[x][y] = 1
                new_state[x][y-2] = 0
                new_state[x][y-1] = 0
                action = f'({x}, {y-2}) -> ({x}, {y})'
                new_states.append((new_state, action))
            if y < 5 and state[x][y+1] == 1 and state[x][y+2] == 1:
                new_state = state.copy()
                new_state[x][y] = 1
                new_state[x][y+2] = 0
                new_state[x][y+1] = 0
                action = f'({x}, {y+2}) -> ({x}, {y})'
                new_states.append((new_state, action))
        return new_states

    def reached_goal(self, state):
        return np.array_equal(state, self.goal_state)


class Agent1:
    def __init__(self, env, heuristic):
        self.frontier = PriorityQueue()
        self.explored = dict()
        self.start_state = env.get_start_state()
        self.goal_state = env.get_goal_state()
        self.env = env
        self.goal_node = None
        self.heuristic = heuristic

    def run(self):
        init_node = Node(parent=None, state=self.start_state, pcost=0, hcost=0)
        self.frontier.push(init_node)
        start = time()
        while not self.frontier.is_empty():
            curr_node = self.frontier.pop()
            if hash(curr_node) in self.explored:
                continue
            self.explored[hash(curr_node)] = curr_node
            if self.env.reached_goal(curr_node.state):
                print("Reached goal!")
                self.goal_node = curr_node
                break
            for state, action in self.env.get_next_states(curr_node.state):
                hcost = self.heuristic(state)
                node = Node(parent=curr_node, state=state, pcost=curr_node.pcost + 1, hcost=hcost, action=action)
                self.frontier.push(node)
        end = time()
        return end - start

    def print_nodes(self):
        node = self.goal_node
        steps = []
        while node:
            steps.append(node)
            node = node.parent
        for step, node in enumerate(reversed(steps), 1):
            print(f"Step: {step}")
            print(node.action)


class Agent2:
    def __init__(self, env, heuristic):
        self.frontier = PriorityQueue()
        self.explored = dict()
        self.start_state = env.get_start_state()
        self.goal_state = env.get_goal_state()
        self.env = env
        self.goal_node = None
        self.heuristic = heuristic

    def run(self):
        init_node = Node(parent=None, state=self.start_state, pcost=0, hcost=0)
        self.frontier.push(init_node)
        start = time()
        while not self.frontier.is_empty():
            curr_node = self.frontier.pop()
            if hash(curr_node) in self.explored:
                continue
            self.explored[hash(curr_node)] = curr_node
            if self.env.reached_goal(curr_node.state):
                print("Reached goal!")
                self.goal_node = curr_node
                break
            for state, action in self.env.get_next_states(curr_node.state):
                hcost = self.heuristic(state)
                node = Node(parent=curr_node, state=state, pcost=0, hcost=hcost, action=action)
                self.frontier.push(node)
        end = time()
        return end - start

    def print_nodes(self):
        node = self.goal_node
        steps = []
        while node:
            steps.append(node)
            node = node.parent
        for step, node in enumerate(reversed(steps), 1):
            print(f"Step: {step}")
            print(node.action)


def heuristic0(curr_state):
    return 0

def heuristic1(curr_state):
    cost = 0
    for i in range(7):
        for j in range(7):
            if curr_state[i][j] == 1:
                cost += abs(i - 3) + abs(j - 3)
    return cost

def heuristic2(curr_state):
    cost = 0
    for i in range(7):
        for j in range(7):
            if curr_state[i][j] == 1:
                cost += 2 ** max(abs(i - 3), abs(j - 3))
    return cost

if __name__ == "__main__":
    env = Environment()
    agent1 = Agent1(env, heuristic2)
    print(f"Runtime: {agent1.run()} s")
    agent1.print_nodes()
