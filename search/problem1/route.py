#!/usr/bin/env python
import sys
import numpy as np
import heapq
from scipy.spatial import distance
#import time

CITY = "city-gps.txt"
ROAD = "road-segments.txt"
MAX_SPEED = 999

# ################
# for extra credit
US_STATE = set( ['_Alabama', '_Alaska', '_Arizona', '_Arkansas',
                 '_California', '_Colorado', '_Connecticut', '_Delaware',
                 '_Florida', '_Georgia', '_Hawaii', '_Idaho',
                 '_Illinois', '_Indiana', '_Iowa', '_Kansas', '_Kentucky',
                 '_Louisiana', '_Maine', '_Maryland', '_Massachusetts',
                 '_Michigan', '_Minnesota', '_Mississippi', '_Missouri',
                 '_Montana', '_Nebraska', '_Nevada', '_New_Hampshire',
                 '_New_Jersey', '_New_Mexico',
                 '_New_York', '_North_Carolina', '_North_Dakota',
                 '_Ohio', '_Oklahoma', '_Oregon', '_Pennsylvania', '_Rhode',
                 '_Island', '_South_Carolina', '_South_Dakota',
                 '_Tennessee', '_Texas', '_Utah', '_Vermont', '_Virginia',
                 '_Washington', '_West', '_Virginia', '_Wisconsin',
                 '_Wyoming'])

class Maps:
    """
        A class for map information,
        including city and road info
    """
    def __init__(self):
        self.city = {}         # vertex
        self.road_graph = {}   # graph: start->end
        self.road_edge = {}    # info with keys

    def add_city(self, city_info):
        self.city[city_info.name] = city_info
        return

    def add_road(self, road_info):
        # bidirection
        if road_info.speed == 0:        #fixed speed limit 0 issue!
            return
        if road_info.start not in self.road_graph:
            self.road_graph[road_info.start] = set()
        if road_info.end not in self.road_graph:
            self.road_graph[road_info.end] = set()
        self.road_graph[road_info.start].add(road_info.end)
        self.road_graph[road_info.end].add(road_info.start)
        self.road_edge[(road_info.start, road_info.end)] = road_info
        self.road_edge[(road_info.end, road_info.start)] = road_info
        return


class City:
    """
        A class for city information
        city: name, gps
    """
    def __init__(self, name, gps=None):
        self.name = name
        self.gps = gps
    
    def gps(self, lat, long):
        self.gps = np.array((lat, long))
        return

    def distance(self, city):
        if city.gps is None:
            return None
        return distance.euclidean(self.gps, city.gps)

class Road:
    """
        A class for road information
        including road: start->end, length, speed, name
    """
    def __init__(self, start, end, length, speed, name):
        self.start = start
        self.end = end
        self.length = length
        self.speed = speed
        self.name = name
        
    def time(self, speed):
        return  length*1.0/speed

def read_maps(city_file, road_file):
    def process_line(line):
        line = line.strip()
        return line.split(" ")
    
    def process_gps(x, y):
        gps = np.array((x, y))
        return gps.astype(float)
    
    def process_city(info):
        city_name = info[0]
        gps = process_gps(info[1], info[2])
        return (city_name, gps)
    
    def process_road(info):
        def convert_float(value):
            try:
                return float(value)
            except ValueError:
                return float("inf")
                        
        start = info[0]
        end = info[1]
        length = info[2]
        speed = info[3]
        name = info[4]
        
        length = convert_float(length)
        speed = convert_float(speed)
        return (start, end, length, speed, name)
    
    # data, d[row][col] = number
    maps = Maps()
    
    # process line by line
    with open(city_file, 'rU') as f:
        for line in f:
            temp = process_line(line)
            param = process_city(temp)
            city = City(*param)
            maps.add_city(city)

    with open(road_file, 'r') as f:
        for line in f:
            temp = process_line(line)
            param = process_road(temp)
            road = Road(*param)
            maps.add_road(road)

    return maps

class State:
    """
        A class for state
        including city and path
    """
    def __init__(self, city_name):
        self.city = city_name
        self.cost = 0
        self.prev = None
        self.path = None
        # for extra credit
        # record all past states
        self.allpath = []

def init_queue():
    return []

def init_vist():
    return set()

def not_empty(queue):
    return len(queue) > 0

def drive_time(state):
    """
        calculate the time driving on road
        for a car that always travels at the speed limit
    """
    time = 0
    while state.prev is not None:
        length = state.path.length
        speed = state.path.speed
        time += length*1.0/speed
        state = state.prev
    return time

def drive_distance(state):
    length = 0
    while state.prev is not None:
        length += state.path.length
        state = state.prev
    return length

def drive_path(state):
    path = []
    while state is not None:
        path.append(state.city)
        state = state.prev
    return path[::-1]


def bdfs_search(start_city, end_city, maps, algo):
    """
        breadth-first search &&
        depth-first search
        (ignores edge weights in the state graph)
    """
    def convert_state(city_name):
        state = State(city_name)
        return state

    def is_goal(state):
        return state.city == end_city

    def insert(queue, state):
        queue.append(state)
        return

    def next_queue(queue):
        if algo == "bfs":
            return queue.pop(0)
        return queue.pop()
    
    def record(visited, state):
        visited.add(state.city)
        return
    
    def not_see(visited, state):
        return state.city not in visited
    
    def successor(state):
        candid = []
    
        if state.city not in maps.road_graph:
            return candid

        for dest in maps.road_graph[state.city]:
            succ = State(dest)
            succ.prev = state
            succ.path = maps.road_edge[(state.city, succ.city)]
            candid.append(succ)
        return candid

    init_state = convert_state(start_city)
    
    # bfs (dfs) search
    if is_goal(init_state):
        return init_state

    # queue-> fringe
    queue = init_queue()
    visited = init_vist()
    insert(queue, init_state)
    while not_empty(queue):
        state = next_queue(queue)
        record(visited, state)
        
        if is_goal(state):
            return state
            
        for succ in successor(state):
            if not_see(visited, succ):
                insert(queue, succ)
    
    return "FAILURE"

def A_star_uniform_search(start_city, end_city, maps, cost_f, algo):
    """
        uniform cost search
        ((the variant of bfs takes edge weights into consideration)
        """
    def convert_state(city_name):
        state = State(city_name)
        return state
    
    def is_goal(state):
        return state.city == end_city
    
    def insert(queue, state, prior):
        heapq.heappush(queue, (prior, state))
        return
    
    def next_queue(queue):
        return heapq.heappop(queue)[1]

    def record(visited, state):
        visited.add(state.city)
        return
    
    def not_see(visited, state):
        return state.city not in visited
    
    def successor(state):
        candid = []
        
        if state.city not in maps.road_graph:
            return candid
        
        for dest in maps.road_graph[state.city]:
            succ = State(dest)
            succ.prev = state
            succ.path = maps.road_edge[(state.city, succ.city)]
            candid.append(succ)
        return candid
    
    def apply_cost_f(cost_f, state, goal, algo):
        # f(n) = g(n) + h(n)
        cost = 0
        if state.prev is not None:
            cost = state.prev.cost
        if cost_f == "segments":
            cost += 1
        elif cost_f == "distance":
            #road = state.path
            cost += state.path.length
        elif cost_f == "time":
            cost += state.path.length*1.0/state.path.speed

        # update state cost
        state.cost = cost
    
        # apply heuristic fun
        if algo == "astar":
            cost += heursitc(state, goal, cost_f)

        return cost

    def heursitc(state, goal, cost_f):
        # calculate the distance between two cities
        if cost_f == "distance":
            if state.city in maps.city \
                and goal in maps.city:
                start = maps.city[state.city]
                dest = maps.city[goal]
                return start.distance(dest)
            return 0
                
        elif cost_f == "time":
            if state.city in maps.city \
                and goal in maps.city:
                start = maps.city[state.city]
                dest = maps.city[goal]
                return start.distance(dest)/MAX_SPEED
            return 0
        
        return 0
    
    # init
    init_state = convert_state(start_city)
    
    # uniform search
    if is_goal(init_state):
        return init_state

    # queue-> fringe
    queue = init_queue()
    visited = init_vist()
    insert(queue, init_state, 0)

    while not_empty(queue):
        state = next_queue(queue)
        record(visited, state)
        
        if is_goal(state):
            return state
        
        for succ in successor(state):
            if not_see(visited, succ):
                insert(queue,
                       succ,
                       apply_cost_f(
                                    cost_f,
                                    succ,
                                    end_city,
                                    algo
                                    )
                       )
    return "FAILURE"

#@profile
def process_search(argv, maps):
    #sanity
    assert(len(argv) == 5)
    progm, start_city, end_city, route_algo, cost_f = argv
    # ###########
    # exctra credit
    if cost_f == "longtour":
        result = long_search(start_city,
                             end_city,
                             maps)
    
    elif cost_f == "statetour":
        result = tour_search(start_city, end_city, maps)
    
    ##############
    elif route_algo == "bfs" or route_algo == "dfs":
        result = bdfs_search(
                             start_city,
                             end_city,
                             maps,
                             route_algo
                             )
    elif route_algo == "uniform" or route_algo == "astar":
        result = A_star_uniform_search(
                                       start_city,
                                       end_city,
                                       maps,
                                       cost_f,
                                       route_algo
                                       )
    return result

# #########
# extra credit
def long_search(start_city, end_city, maps):
    """
        search with additional cost fuction,
        which findnd the longest distance driving path between
        the two cities that does not visit the same city twice.
        
        ATTENTION:
        "the longest path problem is NP-hard"
        -- https://en.wikipedia.org/wiki/Longest_path_problem
        in order to be correct, algorithm
        have to search all possible routes
    """
    def convert_state(city_name):
        state = State(city_name)
        return state
    
    def init_route():
        return []
    
    def is_goal(state):
        return state.city == end_city
    
    def insert(queue, state):
        queue.append(state)
        return
    
    def next_queue(queue):
        return queue.pop()
    
    def successor(state):
        candid = []
        
        if state.city not in maps.road_graph:
            return candid
        
        for dest in maps.road_graph[state.city]:
            succ = State(dest)
            succ.prev = state
            succ.path = maps.road_edge[(state.city, succ.city)]
            candid.append(succ)
        return candid
            
    def record_cost(state):
        # distance
        cost = 0
        if state.prev is not None:
            cost = state.prev.cost
        if state.path is not None:
            cost += state.path.length
        state.cost = cost
        return

    def record_visit(visited, state):
        visited.add(state.city)
        return
    
    def not_see(visited, state):
        return state.city not in visited

    def add_route(route, state):
        route.append(state)
        return
    
    def find_route(route):
        longest = 0
        best = "FAILURE"
        for state in route:
            temp = drive_distance(state)
            if temp > longest:
                best = state
                longest = temp
        return best
    
    # init
    init_state = convert_state(start_city)
    route = init_route()
    
    # queue-> fringe
    queue = init_queue()
    visited = init_vist()
    insert(queue, init_state)

    while not_empty(queue):
        state = next_queue(queue)
        record_cost(state)
        record_visit(visited, state)
        
        if is_goal(state):
            add_route(route, state)
            continue
        
        for succ in successor(state):
            if not_see(visited, succ):
                insert(queue, succ)

    return find_route(route)

def tour_search(start_city, end_city, maps):
    """
        search with additional cost fuction,
        which finnd a route with the shortest total distance
        includes passing through
        at least one city in each of the 48 contiguous U.S. states.
    """
    def convert_state(city_name):
        state = State(city_name)
        return state
                
    def init_route():
        return []
                
    def is_goal(state):
        def passthrough(st):
            pass_states = set([])
            while st is not None:
                temp = st.city.split(',')[1]
                if temp in US_STATE:
                    pass_states.add(temp)
                st = st.prev
            return len(pass_states) > 2
                
        return state.city == end_city and passthrough(state)
                
    def insert(queue, state, prior):
        heapq.heappush(queue, (prior, state))
        return
                
    def next_queue(queue):
        return heapq.heappop(queue)[1]
                
    def successor(state):
        candid = []
                
        if state.city not in maps.road_graph:
            return candid
                
        for dest in maps.road_graph[state.city]:
            succ = State(dest)
            succ.prev = state
            succ.path = maps.road_edge[(state.city, succ.city)]
            succ.allpath = [s for s in state.allpath]
            succ.allpath.append(state.city)
            candid.append(succ)
        return candid

    def record_visit(visited, state):
        temp = "+".join(state.allpath)
        visited.add(temp)
        return
    
    def not_see(visited, state):
        """
            path not traveled,
            if cotains cycles, each cycle should be different
        """
        temp = "+".join(state.allpath)
        return temp not in visited

    def apply_cost(state):
        cost = 0
        if state.prev is not None:
            cost = state.prev.cost
        cost += state.path.length
        state.cost = cost
        
        # heurstic
        cost += heursitc(succ)
        return cost

    def heursitc(state):
        # number of states traveled
        travel = set()
        for s in state.allpath:
            travel.add(s.split(',')[1])
        return 48-len(travel)
    
    # init
    init_state = convert_state(start_city)
    route = init_route()
                
    # queue-> fringe
    queue = init_queue()
    visited = init_vist()
    insert(queue, init_state, 0)
                
    while not_empty(queue):
        state = next_queue(queue)
        record_visit(visited, state)
        #print state.allpath, state.cost
        
        if is_goal(state):
            return state
                
        for succ in successor(state):
            if not_see(visited, succ):
                insert(queue, succ, apply_cost(succ))
                
    return "FAILURE"
    
def nicer_display(result):
    print "The travel times estimate:"
    print "\t\t\t", drive_time(result), "hours"
    print "The whole trips takes:"
    print "\t\t\t", drive_distance(result), "miles"
    print "Enjoy your trip! :-)"
    routes = drive_path(result)
    temp = routes[0].split(",")
    print "start\t", temp[0], "\t\t\t\t@", temp[1][1:]
    routes = routes[1:]
    for interm in routes:
        temp = interm.split(",")
        print "stop at\t", temp[0], "\t\t\t\t@", temp[1][1:]
    print "well done!"
    print
    return

def display(result):
    if result != "FAILURE":
        nicer_display(result)
        temp = []
        temp.append(drive_distance(result))
        temp.append(drive_time(result))
        temp.extend(drive_path(result))
        for item in temp:
            print item,
        print
    else:
        print


# ###########################
# read in data
maps = read_maps(CITY, ROAD)

# process data
#t0 = time.time()
results = process_search(sys.argv, maps)
#t1 = time.time()
#print "runt time is: ", t1-t0

# display movement
display(results)
