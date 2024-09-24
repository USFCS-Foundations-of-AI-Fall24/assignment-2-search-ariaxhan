from queue import PriorityQueue
from Graph import Graph, Edge, Node

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'

    def get_successors(self):
        successors = []
        if self.mars_graph is not None and self.location in self.mars_graph.g:
            for edge in self.mars_graph.g[self.location]:
                cost = edge.val
                new_state = map_state(edge.dest, self.mars_graph, self, self.g + cost)
                successors.append(("move", new_state, cost))
        return successors



def a_star(start_state, heuristic_fn, goal_test_fn, use_closed_list=True):
    search_queue = PriorityQueue()
    closed_list = set()
    search_queue.put(start_state)
    states_generated = 1  # Count the start state

    cost_so_far = {start_state: 0}

    while not search_queue.empty():
        current_state = search_queue.get()

        if goal_test_fn(current_state):
            return reconstruct_path(current_state), states_generated

        if use_closed_list:
            if current_state in closed_list:
                continue
            closed_list.add(current_state)

        for action, next_state, cost in current_state.get_successors():
            new_cost = cost_so_far[current_state] + cost
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                next_state.g = new_cost
                next_state.h = heuristic_fn(next_state)
                next_state.f = next_state.g + next_state.h
                next_state.prev_state = current_state
                search_queue.put(next_state)
                states_generated += 1  # Count each newly generated state

    return None, states_generated

def reconstruct_path(state):
    # create an empty list to store the path
    path = []
    # traverse from the goal state back to the start state
    while state is not None:
        # insert the state at the beginning of the path
        path.insert(0, state)
        # move to the previous state
        state = state.prev_state
    # return the complete path
    return path

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## return the straight-line distance between the state and (1,1)
def sld(state):
    # extract the x and y coordinates from the state's location
    x1, y1 = map(float, state.location.split(','))
    # coordinates of the goal (1,1)
    x2, y2 = 1.0, 1.0
    # calculate the differences in x and y
    dx = x1 - x2
    dy = y1 - y2
    # calculate the straight-line distance using the Euclidean formula
    distance = (dx ** 2 + dy ** 2) ** 0.5
    # return the calculated distance
    return distance

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    mars_graph = Graph()

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            current_node = parts[0]
            neighbors = parts[1].split() if len(parts) > 1 else []

            mars_graph.add_node(current_node)

            for neighbor in neighbors:
                if neighbor not in mars_graph.g:
                    mars_graph.add_node(neighbor)

                # Calculate Euclidean distance
                x1, y1 = map(float, current_node.split(','))
                x2, y2 = map(float, neighbor.split(','))
                distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

                edge = Edge(current_node, neighbor, int(distance))
                mars_graph.add_edge(edge)

                # Add reverse edge if it doesn't exist
                if not mars_graph.get_edge(neighbor, current_node):
                    reverse_edge = Edge(neighbor, current_node, int(distance))
                    mars_graph.add_edge(reverse_edge)

    return mars_graph

def is_goal_state(state):
    return state.is_goal()

def count_states(search_queue, closed_list):
    return search_queue.qsize() + len(closed_list)


# c) **(5 points)** _Sept 18_ Run both A* and uniform cost search (i.e. using h1: h=0 for all states)
# on the MarsMap and count the number of states generated. Add this to your results.

def run(start_location):
    mars_graph = read_mars_graph("marsmap.txt")
    print(f"Start location: {start_location}")
    start_state = map_state(location=start_location, mars_graph=mars_graph)

    print("Running A* search...")
    astar_path, astar_states_generated = a_star(start_state, sld, is_goal_state, use_closed_list=True)

    if astar_path:
        print(f"A* search generated {astar_states_generated} states")
        print(f"A* path length: {len(astar_path)}")
        print("A* path:", [state.location for state in astar_path])
    else:
        print("A* did not find a path")

    start_state = map_state(location=start_location, mars_graph=mars_graph)

    print("\nRunning Uniform Cost Search...")
    ucs_path, ucs_states_generated = a_star(start_state, h1, is_goal_state, use_closed_list=True)

    if ucs_path:
        print(f"Uniform Cost Search generated {ucs_states_generated} states")
        print(f"UCS path length: {len(ucs_path)}")
        print("UCS path:", [state.location for state in ucs_path])
    else:
       print("UCS did not find a path")
