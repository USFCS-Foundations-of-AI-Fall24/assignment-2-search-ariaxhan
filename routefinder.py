from queue import PriorityQueue
from Graph import Graph, Edge

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


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
     # create a priority queue to hold the states to explore
    search_queue = PriorityQueue()
    # create a dictionary to keep track of explored states
    closed_list = {}
    # put the start state into the priority queue
    search_queue.put(start_state)

    # create a dictionary to keep track of cost so far for each state
    cost_so_far = {}
    # initialize the cost for the start state to zero
    cost_so_far[start_state] = 0

    while not search_queue.empty():
        # get the state with the lowest priority (f value)
        current_state = search_queue.get()
        # check if the current state is the goal
        if goal_test(current_state):
            # if so, reconstruct and return the path from start to goal
            return reconstruct_path(current_state)

        if use_closed_list:
            # if we've already explored this state, skip it
            if current_state in closed_list:
                continue
                # mark the current state as explored
                closed_list[current_state] = True

        # generate successors of the current state
        for action, next_state, cost in current_state.get_successors():
            # calculate the new cost to reach the next state
            new_cost = cost_so_far[current_state] + cost
            # if next state is unexplored or we found a cheaper path
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                # update the cost to reach the next state
                cost_so_far[next_state] = new_cost
                # update the g, h, and f values of the next state
                next_state.g = new_cost
                next_state.h = heuristic_fn(next_state)
                next_state.f = next_state.g + next_state.h
                # set the previous state for path reconstruction
                next_state.prev_state = current_state
                # add the next state to the priority queue
                search_queue.put(next_state)

      # if we reach here, no path was found
    return None

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

    # open the file and read each line
    with open(filename, 'r') as file:
        for line in file:
            # split into parts
            parts = line.strip().split()
            # current node is first part
            current_node = parts[0]

            # add the current node to the graph
            mars_graph.add_node(current_node)

            # process the neighbors and their distances
            for i in range(1, len(parts), 2):
                neighbor = parts[i]
                distance = int(parts[i+1])

                # add the neighbor node if it doesn't exist
                if neighbor not in mars_graph.g:
                    mars_graph.add_node(neighbor)

                # add the edge from current_node to neighbor
                edge = Edge(current_node, neighbor, distance)
                mars_graph.add_edge(edge)

                # add the reverse edge (assuming undirected graph)
                reverse_edge = Edge(neighbor, current_node, distance)
                mars_graph.add_edge(reverse_edge)

    return mars_graph


# c) **(5 points)** _Sept 18_ Run both A* and uniform cost search (i.e. using h1: h=0 for all states)
# on the MarsMap and count the number of states generated. Add this to your results.

def run(start_location):
    # Read the Mars graph
    mars_graph = read_mars_graph("marsmap.docx")

    # Create the initial state
    start_state = map_state(location=start_location, mars_graph=mars_graph)


    # Run A* search
    print("Running A* search...")


    print(f"A* search generated {astar_states_generated} states")
    print("A* path:", [state.location for state in astar_path])

    # Reset for Uniform Cost Search

    # Run Uniform Cost Search (using h1 heuristic)
    print("\nRunning Uniform Cost Search...")


    print(f"Uniform Cost Search generated {ucs_states_generated} states")
    print("Uniform Cost Search path:", [state.location for state in ucs_path])
