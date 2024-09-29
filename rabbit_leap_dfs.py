class RabbitLeapProblemDFS:
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

    def dfs(self):

        return self._dfs_helper(self.initial_state, [])
    
    def _dfs_helper(self, state, path):

        if self.is_goal(state):
            return path + [state]
        

        for successor in self.get_successors(state):
            if successor not in path:
                result = self._dfs_helper(successor, path + [state])
                if result:
                    return result
        
        return None 

# Example usage:
problem_dfs = RabbitLeapProblemDFS(INITIAL_STATE, GOAL_STATE)
solution_dfs = problem_dfs.dfs()
if solution_dfs:
    print("DFS Solution path:")
    print_solution(solution_dfs)
else:
    print("No solution found.")
