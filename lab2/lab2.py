from oliverj_utils.timing import Timing, Tree

tree=Tree()
timing=Timing(tree)

# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
# ANSWER1 = True
# ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from oliverj_utils.timing import TIMING

timing = TIMING


## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

class Search(object):

    def __init__(self, graph: Graph, start: str, goal: str):
        self.agenda = list()
        self.graph = graph
        self.start = start
        self.goal = goal
        self.push([self.start])  # initialize with starting node as first path
    @timing.time
    def clear_agenda(self) -> None:
        self.agenda = []
    @timing.time
    def pop(self, index: int = -1) -> list:
        if len(self.agenda) == 0:
            return None
        elif index != 0 and index != -1:
            raise ValueError("Pop can only remove the first or last element (index 0 or -1)")
        else:
            return self.agenda.pop(index)
    @timing.time
    def push(self, path: list) -> None:
        if len(path) == 0:
            raise ValueError("You cannot add a zero length path to the agenda")
        self.agenda.append( path )

    ## append a path to the tail of the agenda
    @timing.time
    def enqueue(self, path: list) -> None:
        self.push(path)

    ## remove a path from the front of the agenda
    @timing.time
    def dequeue(self) -> list:
        return self.pop(0)
    @timing.time
    def peek(self, index: int = -1) -> list:
        if len(self.agenda) == 0:
            return None
        elif index != 0 and index != -1:
            raise ValueError("Peek can only look at first or last element (index 0 or -1)")
        else:
            return self.agenda[index]
    @timing.time
    def peek_front(self) -> list:
        return self.peek(0)
    @timing.time
    def peek_tail(self) -> list:
        return self.peek()
    @timing.time
    def peek_top(self) -> list:
        return self.peek_tail()
    @timing.time
    def length(self) -> int:
        return len(self.agenda)

    def __str__(self) -> str:
        return self.agenda.__str__()

    @timing.time
    def bfs(self) -> list:
        @timing.time
        def remove_func(search):
            return search.dequeue()
        @timing.time
        def add_func(search, next_path: list):
            search.enqueue(next_path)

        return self.generic_search(remove_func, add_func)

    @timing.time
    def dfs(self) -> list:
        @timing.time
        def remove_func(search):
            return search.pop()
        @timing.time
        def add_func(search, next_path: list):
            search.push(next_path)

        return self.generic_search(remove_func, add_func)

    @timing.time
    def hill_climbing(self) -> list:
        @timing.time
        def remove_func(search):
            return search.pop()
        @timing.time
        def add_func(search, next_path: list):
            search.push(next_path)

        @timing.time
        def sort_func(nodes: list):
            @timing.time
            def order_func(val):
                return self.graph.get_heuristic(val, self.goal)

            nodes.sort(key=order_func, reverse=True)

        return self.generic_search(remove_func, add_func, sort_func)

    @timing.time
    def beam_search(self, beam_width) -> list:

        @timing.time
        def remove_func(search):
            r = search.dequeue()
            return r

        @timing.time
        def add_func(search, next_path: list):
            search.enqueue(next_path)

        def sort_func(nodes: list):
            @timing.time
            def order_func(val):
                return self.graph.get_heuristic(val, self.goal)

            nodes.sort(key=order_func, reverse=False)

        # remove nodes from agenda until we have only beam_widgth left
        @timing.time
        def mutate_func():
            while len(self.agenda) > beam_width:
                del self.agenda[-1]

        return self.generic_search(remove_func, add_func, sort_func, mutate_func)

    @timing.time
    def branch_and_bound(self) -> list:
        @timing.time
        def remove_func(search):
            return search.dequeue()

        @timing.time
        def add_func(search, next_path: list):
            search.enqueue(next_path)

        # sort the agenda by path length
        @timing.time
        def mutate_func():
            @timing.time
            def order_func(val):
                return path_length(self.graph, val)

            self.agenda.sort(key=order_func, reverse=False)

        return self.generic_search(remove_func, add_func, None, mutate_func)

    @timing.time
    def a_star(self) -> list:
        self.counter = 0

        @timing.time
        def remove_func(search):
            return search.dequeue()

        @timing.time
        def add_func(search, next_path: list):
            search.enqueue(next_path)

        @timing.time
        def mutate_func():
            min_paths = dict()
            self.counter=self.counter+1
            
            # first evaluate every path in agenda that goes through a common node
            # keep only paths that have reach common node with least cost            
            for path in self.agenda:
                for node in path:
                    distance = path_length(self.graph,path,node)        
                    if( not node in min_paths or distance < min_paths[node][0] ):
                        min_paths[node] = (distance,path)
            
            filtered_agenda = list()
            for (node, t) in min_paths.items():
                distance = t[0]
                path = t[1]
                if path not in filtered_agenda:
                    filtered_agenda.append(path)

            self.agenda = filtered_agenda

            # then sort the agenda by cost, ascending
            @timing.time
            def order_func(val):
                return (path_length(self.graph, val) +
                        self.graph.get_heuristic(val[-1], self.goal))

            self.agenda.sort(key=order_func, reverse=False)

        return self.generic_search(remove_func,add_func,None,mutate_func)

    @timing.time
    def generic_search(self, remove_func, add_func, sort_func=None, mutate_func=None) -> list:

        while self.length() > 0:

            current_path = remove_func(self)

            # if the last node in the current path is goal, then we're done
            last_node = current_path[-1]
            if last_node == self.goal:
                return current_path

            # obtain the list of next nodes (skipping any that are already in current path)
            next_nodes = [next for next 
                in self.graph.get_connected_nodes(last_node) 
                if not next in current_path]

            # if a sorting function has been provided, then apply it
            if sort_func is not None:
                sort_func(next_nodes)

            # enqueue paths to connected nodes
            for next in next_nodes:
                next_path = current_path.copy()
                next_path.append(next)
                add_func(self,next_path)

            # if an agenda mutation function has been provided, then apply it
            if mutate_func is not None:
                next_nodes = mutate_func()

        # no path found, return empty list
        return []

@timing.time
def bfs(graph, start, goal):
    search = Search(graph, start, goal)
    return search.bfs()

@timing.time
def dfs(graph, start, goal):
    search = Search(graph, start, goal)
    return search.dfs()


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
@timing.time
def hill_climbing(graph, start, goal):
    search = Search(graph, start, goal)
    return search.hill_climbing()


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
@timing.time
def beam_search(graph, start, goal, beam_width):
    search = Search(graph, start, goal)
    return search.beam_search(beam_width)


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
@timing.time
def path_length(graph, node_names, stop_node=None):
    path_length = 0
    for count, node in enumerate(node_names):
        if node == stop_node:
            break
        if len(node_names) > (count + 1):
            edge = graph.get_edge(node, node_names[count + 1])
            path_length += edge.length
    return path_length


@timing.time
def branch_and_bound(graph, start, goal):
    search = Search(graph, start, goal)
    return search.branch_and_bound()


@timing.time
def a_star(graph, start, goal):
    search = Search(graph, start, goal)
    return search.a_star()


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

@timing.time
def is_admissible(graph, goal):
    if goal in graph.heuristic.keys():
        for start in graph.heuristic[goal].keys():
            search = Search(graph, start, goal)
            path = search.branch_and_bound()
            length = path_length(graph, path)
            if graph.heuristic[goal][start] > length:
                return False
    return True

@timing.time
def is_consistent(graph, goal):
    if goal in graph.heuristic:
        for start, h1 in graph.heuristic[goal].items():
            connected_nodes = graph.get_connected_nodes(start)
            for node in connected_nodes:
                length = graph.get_edge(start,node).length
                h2 = 0
                if node in graph.heuristic[goal]:
                    h2 = graph.heuristic[goal][node]
                if h1 > (h2+length):
                    return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '8'
WHAT_I_FOUND_INTERESTING = 'Creating a generic search function'
WHAT_I_FOUND_BORING = 'Trying to visualize a graph from the data'
