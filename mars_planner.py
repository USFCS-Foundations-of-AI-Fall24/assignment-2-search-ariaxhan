## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy
from search_algorithms import breadth_first_search
from search_algorithms import depth_first_search

class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, charged=False, holding_tool=False):
        self.loc = loc
        self.sample_extracted=sample_extracted
        self.holding_sample = holding_sample
        self.charged=charged
        self.holding_tool = holding_tool
        self.prev = None

    ## you do this.
    def __eq__(self, other):
       return (self.loc == other.loc and
                self.sample_extracted == other.sample_extracted and
                self.holding_sample == other.holding_sample and
                self.charged == other.charged and
                self.holding_tool == other.holding_tool)


    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n" +
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Holding Tool?: {self.holding_tool}\n" +
                f"Charged? {self.charged}")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        succ = [(item(self), item.__name__) for item in list_of_actions]
        ## remove actions that have no effect
        succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.
def move_to_sample(state):
    if state.loc != "sample":
        r2 = deepcopy(state)
        r2.loc = "sample"
        r2.prev = state
        return r2
    else:
        return state  # No change

def move_to_station(state):
    if state.loc != "station":
        r2 = deepcopy(state)
        r2.loc = "station"
        r2.prev = state
        return r2
    else:
        return state

def move_to_battery(state):
    if state.loc != "battery":
        r2 = deepcopy(state)
        r2.loc = "battery"
        r2.prev = state
        return r2
    else:
        return state


# add tool functions here
def pick_up_tool(state) :
    # return a new state with the holding_tool variable set to True
    if state.loc == "station" and not state.holding_tool:
          r2 = deepcopy(state)
          r2.holding_tool = True
          r2.prev = state
          return r2
    else:
          return state
def drop_tool(state) :
    # return a new state with the holding_tool variable set to false
    if state.holding_tool and state.loc == "station":
         r2 = deepcopy(state)
         r2.holding_tool = False
         r2.prev = state
         return r2
    else:
         return state
def use_tool(state) :
    # return a new state with the sample_extracted variable set to True
    if state.holding_tool and state.loc == "sample" and not state.sample_extracted:
        r2 = deepcopy(state)
        r2.sample_extracted = True
        r2.prev = state
        return r2
    else:
        return state

def pick_up_sample(state) :
    if state.sample_extracted and state.loc == "sample" and not state.holding_sample:
        r2 = deepcopy(state)
        r2.holding_sample = True
        r2.prev = state
        return r2
    else:
        return state

def drop_sample(state) :
    if state.holding_sample and state.loc == "station":
        r2 = deepcopy(state)
        r2.holding_sample = False
        r2.prev = state
        return r2
    else:
        return state

def charge(state):
    if state.loc == "battery" and not state.charged:
        r2 = deepcopy(state)
        r2.charged = True
        r2.prev = state
        return r2
    else:
        return state

action_list = [charge, drop_sample, pick_up_sample, move_to_sample, move_to_battery, move_to_station,
               pick_up_tool, drop_tool, use_tool]

# goals
def battery_goal(state) :
    return state.loc == "battery"

def sample_holding_goal(state) :
    return state.holding_sample

def charged_goal(state) :
    return state.charged


# decomposing the problem: define new goals moveToSample, removeSample, and returnToCharger

def at_sample_goal(state):
    return state.loc == "sample" and state.holding_tool

def sample_extracted_goal(state):
    return state.sample_extracted

def at_charger_goal(state):
    return state.loc == "battery" and state.charged

# define new sublists of actions for each subgoal

move_to_sample_actions = [pick_up_tool, move_to_sample]
remove_sample_actions = [use_tool, pick_up_sample, move_to_station, drop_sample, drop_tool, move_to_sample]
return_to_charger_actions = [move_to_battery, charge, drop_tool, drop_sample]

def mission_complete(state) :
    # returns True if we are at the battery, charged, and the sample is at the station.
    return (state.loc == "battery" and
            state.charged == True and
            state.holding_sample == False and
            state.sample_extracted == True)

def main():
    s = RoverState()
    # BFS
    result_bfs = breadth_first_search(s, action_list, mission_complete)
    print("Breadth First Search Result:", result_bfs)
    # DFS
    result_dfs = depth_first_search(s, action_list, mission_complete)
    print("Depth First Search Result:", result_dfs)
    # DLS
    result_dls = depth_first_search(s, action_list, mission_complete, limit=10, isDLS=True)
    print("Depth Limited Search Result:", result_dls)

    print("\nDecomposed Problem Solutions")

    # Subproblem 1: Move to Sample
    print("\nSubproblem 1: Move to Sample")
    # BFS
    result_sub1_bfs = breadth_first_search(s, move_to_sample_actions, at_sample_goal)
    print("Subproblem 1 BFS Result:", result_sub1_bfs)
    # DFS
    result_sub1_dfs = depth_first_search(s, move_to_sample_actions, at_sample_goal)
    print("Subproblem 1 DFS Result:", result_sub1_dfs)

    # Subproblem 2: Remove Sample
    print("\nSubproblem 2: Remove Sample")
    # Start states are the results from Subproblem 1
    if result_sub1_bfs is not None:
        start_state_sub2_bfs = result_sub1_bfs[0]
        result_sub2_bfs = breadth_first_search(start_state_sub2_bfs, remove_sample_actions, sample_extracted_goal)
        print("Subproblem 2 BFS Result:", result_sub2_bfs)
    else:
        print("Subproblem 1 BFS failed; cannot proceed to Subproblem 2 BFS")

    if result_sub1_dfs is not None:
        start_state_sub2_dfs = result_sub1_dfs[0]
        result_sub2_dfs = depth_first_search(start_state_sub2_dfs, remove_sample_actions, sample_extracted_goal)
        print("Subproblem 2 DFS Result:", result_sub2_dfs)
    else:
        print("Subproblem 1 DFS failed; cannot proceed to Subproblem 2 DFS")

    # Subproblem 3: Return to Charger
    print("\nSubproblem 3: Return to Charger")
    # BFS
    if result_sub2_bfs is not None:
        start_state_sub3_bfs = result_sub2_bfs[0]
        result_sub3_bfs = breadth_first_search(start_state_sub3_bfs, return_to_charger_actions, at_charger_goal)
        print("Subproblem 3 BFS Result:", result_sub3_bfs)
    else:
        print("Subproblem 2 BFS failed; cannot proceed to Subproblem 3 BFS")

    # DFS
    if result_sub2_dfs is not None:
        start_state_sub3_dfs = result_sub2_dfs[0]
        result_sub3_dfs = depth_first_search(start_state_sub3_dfs, return_to_charger_actions, at_charger_goal)
        print("Subproblem 3 DFS Result:", result_sub3_dfs)
    else:
        print("Subproblem 2 DFS failed; cannot proceed to Subproblem 3 DFS")

if __name__ == "__main__":
    main()
