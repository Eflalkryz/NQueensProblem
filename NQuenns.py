import random
from simpleai.search.models import SearchProblem
from simpleai.search import breadth_first, depth_first, uniform_cost, limited_depth_first, iterative_limited_depth_first, astar, greedy
from simpleai.search.local import hill_climbing, hill_climbing_random_restarts, genetic

class NQueens(SearchProblem):
    def __init__(self, N, initial_state=None):
        self.N = N
        if initial_state is None:
            self._set_state()
        else:
            self.state = tuple(map(int, initial_state))
        super().__init__(tuple(self.state))  # Initial state is a tuple of queen positions

    def actions(self, state):
        return [(i, j) for i in range(1, self.N + 1) for j in range(1, self.N + 1)]

    def result(self, state, action):
        i, j = action
        new_state = list(state)
        new_state[i - 1] = j
        return tuple(new_state)

    def is_goal(self, state):
        return self._count_attacking_pairs(state) == 0

    def heuristic(self, state):
        return self._count_attacking_pairs(state)
    
    def generate_random_state(self):
        random_state = ""
        for _ in range(self.N):
            str_val = random.randint(1, self.N)
            random_state += str(str_val)
        return random_state
    

    def _set_state(self):
        state_answer = input("Enter 1 for Manual Entrance, 0 for Random State:")
        if state_answer == "0":
            self.state = self.generate_random_state()
        elif state_answer == "1":
            state_temp = input("enter state: ")
            if self._is_valid(state_temp):
                self.state = state_temp
            else:
                self.state = "wrong state"
        else:
            self.state = "wrong entry"
            
    def _count_attacking_pairs(self, state):
        if self._is_valid(self.state):
            attacking_pairs = 0
            for index, state_indexed in enumerate(state):
                for index1, state_indexed1 in enumerate(state):
                    if index < index1:
                        coordinate = [index + 1, int(state_indexed)]
                        coordinate_1 = [index1 + 1, int(state_indexed1)]
                        if (abs(coordinate[0] - coordinate_1[0]) == abs(coordinate[1] - coordinate_1[1])) or \
                                (coordinate[0] == coordinate_1[0]) or (coordinate[1] == coordinate_1[1]):
                            attacking_pairs += 1 
            return attacking_pairs
        return "Error"
    
    def _is_valid(self, state):
        if len(state) != self.N:
            print("The length of the state string is not equal to N.")
            return False
        for i in range(len(state)):
            try:
                if not 1 <= int(state[i]) <= self.N:
                    print("State string includes numbers greater than N or less than 1.")
                    return False
            except ValueError:
                return False
        return True
    
    def value(self, state):
        return -self._count_attacking_pairs(state)

    def crossover(self, state1, state2):
        crossover_point = random.randint(1, self.N - 1)
        new_state = state1[:crossover_point] + state2[crossover_point:]
        return new_state

    def mutate(self, state):
        index_to_mutate = random.randint(0, self.N - 1)
        new_state = list(state)
        new_state[index_to_mutate] = str(random.randint(1, self.N))
        return ''.join(new_state)
    
            
    def solve_with_algorithm(self, algorithm_name):
        result=None
        algorithm = None
        if algorithm_name == 'bfs':
            algorithm = breadth_first
        elif algorithm_name == 'ucs':
            algorithm = uniform_cost
        elif algorithm_name == 'dfs':
            algorithm = depth_first
        elif algorithm_name == 'dls':
            limit = int(input("Enter depth limit for DLS: "))
            algorithm = limited_depth_first
            result = limited_depth_first(self, depth_limit=limit)
        elif algorithm_name == 'ids':
            algorithm = iterative_limited_depth_first
        elif algorithm_name == 'greedy':
            algorithm = greedy
        elif algorithm_name == 'astar':
            algorithm = astar
        if algorithm_name == 'genetic':
            algorithm = genetic
            result = genetic(self)
        elif algorithm_name == 'hill_climbing':
            algorithm = hill_climbing
            result = hill_climbing(self)
        elif algorithm_name == 'random_restart_hill_climbing':
            limit = int(input("Enter a restart limit for random hill climbing: "))
            algorithm = hill_climbing_random_restarts
            result = hill_climbing_random_restarts(self, restarts_limit=limit)

        if algorithm:
            problem = NQueens(self.N, self.state)
            if result is None:
                result = algorithm(problem, graph_search=graph_search)

            print(f"\nAlgorithm: {algorithm_name}")
            print(f"Resulting State: {result.state}")
            print(f"Resulting Path: {result.path()}")
            print(f"Cost: {result.cost}")
            if hasattr(result, 'nodes'):
                print(f"Viewer Statistics: Max Fringe Size: {result.nodes['max_fringe_size']}, Visited Nodes: {result.nodes['visited_nodes']}")
            else:
                print("Viewer statistics not available for this algorithm.")
            
        else:
            print("Invalid algorithm name. Please enter a valid algorithm.")

if __name__ == "__main__":
    N = int(input("Enter the size of the chessboard (N): "))
    algorithm_name = input("Enter the algorithm name (BFS, UCS, DFS, DLS, ids, Greedy, astar, genetic, hill_climbing, random_restart_hill_climbing): ").lower()
    graph_search = input("Use graph search? (yes or no): ").lower() == 'yes'
    
    queens_problem = NQueens(N)
    queens_problem.solve_with_algorithm(algorithm_name)