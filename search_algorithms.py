from collections import deque



## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True

    states_generated = 1  # Count the start state

    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            print(f"BFS generated {states_generated} states.")
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            states_generated += len(successors)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=20, isDLS=False) :
    search_queue = deque()
    closed_list = {}
    search_queue.append((startState,"", 0))
    if use_closed_list :
        closed_list[startState] = True
    states_generated = 1  # Count the start state
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        if next_state[2] >= limit:  # Skip states that have reached the depth limit
            continue
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            if not isDLS:
                print(f"DFS generated {states_generated} states.")
            else:
                print(f"DLS generated {states_generated} states.")
            return next_state
        else :
            successors = [(s[0], s[1], next_state[2] + 1) for s in next_state[0].successors(action_list)]
            states_generated += len(successors)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]

                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)
