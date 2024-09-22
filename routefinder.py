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
    while not search_queue.empty():
          # get the state with the lowest priority (f value)
          current_state = search_queue.get()

          # check if the current state is the goal
          if goal_test(current_state):
              # reconstruct and return the path from start to goal
              return reconstruct_path(current_state)

          if use_closed_list:
              # if we've already explored this state, skip it
              if current_state in closed_list:
                  continue
              # mark the current state as explored
              closed_list[current_state] = True

          # generate successors of the current state
          for action, next_state, cost in current_state.get_successors():

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

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    sqt(a^ + b2)

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
