from collections import deque

INITIAL_STATE = ['E', 'E', 'E', '_', 'W', 'W', 'W']
GOAL_STATE = ['W', 'W', 'W', '_', 'E', 'E', 'E']

class RabbitLeapProblem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def is_goal(self, state):
        return state == self.goal_state
    
    def get_successors(self, state):
        successors = []
        empty_index = state.index('_')
        
        # Generate all valid moves
        for i in range(len(state)):
            if state[i] == 'E': 
                if i + 1 == empty_index:  
                    new_state = state[:]
                    new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                    successors.append(new_state)
                elif i + 2 == empty_index and state[i + 1] == 'W':  
                    new_state = state[:]
                    new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                    successors.append(new_state)
            elif state[i] == 'W': 
                if i - 1 == empty_index: 
                    new_state = state[:]
                    new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                    successors.append(new_state)
                elif i - 2 == empty_index and state[i - 1] == 'E': 
                    new_state = state[:]
                    new_state[i], new_state[empty_index] = new_state[empty_index], new_state[i]
                    successors.append(new_state)
        
        return successors

    def bfs(self):
  
        frontier = deque([(self.initial_state, [])]) 
        explored = set()
        explored.add(tuple(self.initial_state))
        
        while frontier:
            state, path = frontier.popleft()
           
            if self.is_goal(state):
                return path + [state]
          
            for successor in self.get_successors(state):
                if tuple(successor) not in explored:
                    explored.add(tuple(successor))
                    frontier.append((successor, path + [state]))
        
        return None  

def print_solution(path):
    for state in path:
        print(state)


problem = RabbitLeapProblem(INITIAL_STATE, GOAL_STATE)
solution = problem.bfs()
if solution:
    print("BFS Solution path:")
    print_solution(solution)
else:
    print("No solution found.")
