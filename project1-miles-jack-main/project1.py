"""
 *****************************************************************************
    FILE:       project1.py
    AUTHOR:      Miles Wyner, Jack Kaffenbarger, Carter Steckbeck
    ASSIGNMENT:  Project 1
    DATE:        February 22, 2021
    DESCRIPTION:

    input:                 python3 project1.py env_k algorithm search_type
        env_k:            (0-6)
        algorithm:        (BFS, DFS, IDS, GBFS, AStar)
        search_type:      (graph, tree)
        visualize path?:  (0=no, 1=yes)
        example input:    'python3 project1.py 3 BFS graph 1'

    output:
        number of nodes generated: (time complexity)
        maximum nodes stored:      (space complexity)
        pathway taken by agent:    (optimality)
        visualization of pathway:  (a lil extra fun)

*****************************************************************************
"""


from vacuum_environment import VacuumEnvironment
from hw1 import VacuumEnvironment375
import copy
from queue import LifoQueue
import heapq
import sys
import turtle
# import pandas as pd


class Bode:

    def __init__(self, state, parent, action, path_cost, heuristic_val):
        self.state = state # the environment
        self.parent = parent # also order of solution through traceback
        self.action = action # action taken to reach node from parent
        self.path_cost = path_cost # total path cost to reach given state
        self.heuristic_val = heuristic_val # value computed by heuristic

    def __lt__(self, other):
        return self.heuristic_val < other.heuristic_val


def animate_path_taken(env, path):
    side_length = 70
    turtle.right(90)
    turtle.speed(0)
    for col in range(env.cols):
        turtle.penup()
        turtle.setpos(-200 + (col * side_length), 200)
        turtle.pendown()
        for row in range(env.rows):
            if env.__getitem__((row, col)) == "Dirt":
                turtle.color("light salmon")
            elif env.__getitem__((row, col)) == "Obstacle":
                turtle.color("dark slate gray")
            elif env.__getitem__((row, col)) == "Empty":
                turtle.color("silver")
            elif env.__getitem__((row, col)) == "Agent":
                agent = (row, col)
                turtle.color("medium purple")
            turtle.begin_fill()
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.end_fill()
    turtle.penup()
    turtle.setpos(-200 + (agent[0] * side_length), 200 - (agent[0] * side_length))
    turtle.pendown()
    # turtle.pendown()
    count = 0
    for dir in path:
        turtle.penup()
        turtle.setheading(270)
        turtle.color("silver")
        turtle.pendown()
        turtle.begin_fill()
        turtle.forward(side_length)
        turtle.left(90)
        turtle.forward(side_length)
        turtle.left(90)
        turtle.forward(side_length)
        turtle.left(90)
        turtle.forward(side_length)
        turtle.end_fill()
        turtle.penup()
        turtle.setheading(270)
        turtle.forward(side_length / 2)
        turtle.left(90)
        turtle.forward(side_length / 2)
        turtle.pendown()
        turtle.color("black")
        turtle.write(str(count), False, align="center")
        turtle.penup()
        turtle.setheading(180)
        turtle.forward(side_length / 2)
        turtle.right(90)
        turtle.forward(side_length / 2)
        turtle.color("medium purple")
        turtle.begin_fill()
        if dir == "U":
            turtle.setheading(90)
            turtle.pendown()
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
        if dir == "L":
            turtle.setheading(180)
            turtle.pendown()
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
        if dir == "D":
            turtle.setheading(270)
            turtle.forward(side_length)
            turtle.pendown()
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
            turtle.left(90)
            turtle.forward(side_length)
        if dir == "R":
            turtle.setheading(0)
            turtle.forward(side_length)
            turtle.pendown()
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
            turtle.right(90)
            turtle.forward(side_length)
        turtle.end_fill()
        count+=1
    turtle.penup()
    turtle.setheading(270)
    turtle.forward(side_length / 2)
    turtle.left(90)
    turtle.forward(side_length / 2)
    turtle.pendown()
    turtle.color("black")
    turtle.write(str(count), False, align="center")
    turtle.hideturtle()
    turtle.exitonclick()
    return


def BFS(search, state):

    if search == "tree":
        frontier = [Bode(state, None, None, 0, None)]
        nodes_generated = 1
        max_nodes_stored = 1
        curr_nodes_stored = 1

        while True:
            for letter in "UDRL":
                temp_state = copy.deepcopy(state)
                temp_state.move_agent(letter)

                if temp_state.agent_loc != state.agent_loc: # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = frontier[0]
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    frontier.append(Bode(temp_state, # add new state to frontier
                                         frontier[0],
                                         letter,
                                         frontier[0].path_cost + 1,
                                         None))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

            # perform BFS on next environment
            frontier.pop(0)
            max_nodes_stored -= 1
            state = frontier[0].state

        print("search unable to find a solution.")
        return

    if search == "graph":
        frontier = [Bode(state, None, None, 0, None)]
        explored_set = {state.__hash__()}
        nodes_generated = 1
        max_nodes_stored = 1
        curr_nodes_stored = 1

        while True:
            for letter in "UDRL":
                temp_state = copy.deepcopy(state)
                temp_state.move_agent(letter)

                # agent moved, new state acheieved
                if (temp_state.agent_loc != state.agent_loc and
                    temp_state.__hash__() not in explored_set):

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = frontier[0]
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    explored_set.add(temp_state.__hash__())
                    frontier.append(Bode(temp_state, # add new state to frontier
                                         frontier[0],
                                         letter,
                                         frontier[0].path_cost + 1,
                                         None))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

            # perform BFS on next environment
            frontier.pop(0)
            max_nodes_stored -= 1
            state = frontier[0].state

        print("search unable to find a solution.")
        return


def DFS(search, state):

    if search == "tree":
        stack = LifoQueue (maxsize = 0)
        stack.put(Bode(state, None, None, 0, None))
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            top = stack.get() # perform DFS on next environment (pop)
            curr_nodes_stored -= 1

            for letter in "UDRL":
                temp_state = copy.deepcopy(state)
                temp_state.move_agent(letter)

                if temp_state.agent_loc != state.agent_loc: # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    stack.put(Bode(temp_state, # add new state to stack
                                         state,
                                         letter,
                                         top.path_cost + 1,
                                         None))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

        print("search unable to find a solution.")
        return

    if search == "graph":
        stack = LifoQueue (maxsize = 0)
        stack.put(Bode(state, None, None, 0, None))
        explored_set = {state.__hash__()}
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            curr_Bode = stack.get() # perform DFS on next environment (pop)
            curr_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                if (temp_state.agent_loc != curr_state.agent_loc and
                    temp_state.__hash__() not in explored_set): # agent moved

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # print(temp_state.__str__()) # print if agent moves

                    # add new state to stack (push) and explored set
                    stack.put(Bode(temp_state,
                                   curr_Bode,
                                   letter,
                                   curr_Bode.path_cost + 1,
                                   None))
                    explored_set.add(temp_state.__hash__())

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored


        print("search unable to find a solution.")
        return


def IDS(search, state, depth_limit = 0):

    if search == "tree":
        stack = LifoQueue (maxsize = 0)
        stack.put(Bode(state, None, None, 0, None))
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            # recurse if no solution found within depth limit
            if stack.empty():
                return IDS(search, state, depth_limit + 1)

            curr_Bode = stack.get() # perform DFS on next environment (pop)
            curr_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                # dont add nodes to stack after depth limit
                if (curr_Bode.path_cost + 1 > depth_limit):
                    break

                if (temp_state.agent_loc != curr_state.agent_loc): # agent moved

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # print(temp_state.__str__()) # print if agent moves

                    # add new state to stack (push)
                    stack.put(Bode(temp_state,
                                   curr_Bode,
                                   letter,
                                   curr_Bode.path_cost + 1,
                                   None))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored


        print("search unable to find a solution.")
        return

    if search == "graph":
        stack = LifoQueue (maxsize = 0)
        stack.put(Bode(state, None, None, 0, None))
        explored_set = {state.__hash__()}
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:

            # recurse if no solution found within depth limit
            if stack.empty():
                return IDS(search, state, depth_limit + 1)

            curr_Bode = stack.get() # perform DFS on next environment (pop)
            curr_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                # stop at depth limit
                if (curr_Bode.path_cost + 1 > depth_limit):
                    break

                if (temp_state.agent_loc != curr_state.agent_loc and
                    temp_state.__hash__() not in explored_set): # agent moved

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # print(temp_state.__str__()) # print if agent moves

                    # add new state to stack (push) and explored set
                    stack.put(Bode(temp_state,
                                   curr_Bode,
                                   letter,
                                   curr_Bode.path_cost + 1,
                                   None))
                    explored_set.add(temp_state.__hash__())

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored


        print("search unable to find a solution.")
        return


def GBFS(search, state):

    if search == "tree":
        priority_queue = [Bode(state, None, None, 0, state.heuristic1())]
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            curr_Bode = heapq.heappop(priority_queue) # get next node from q
            max_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                if temp_state.agent_loc != curr_state.agent_loc: # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:

                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # add new state to priority queue
                    heapq.heappush(priority_queue,
                                  Bode(temp_state,
                                        curr_Bode,
                                        letter,
                                        curr_Bode.path_cost + 1,
                                        temp_state.heuristic1()))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

        print("search unable to find a solution.")
        return

    if search == "graph":
        priority_queue = [Bode(state, None, None, 0, state.heuristic1())]
        explored_set = {state.__hash__()}
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            curr_Bode = heapq.heappop(priority_queue) # pop off node next in q
            max_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                if (temp_state.agent_loc != curr_state.agent_loc and
                    temp_state.__hash__() not in explored_set): # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print(temp_state.__str__())
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # add new state to priority queue and explored set
                    heapq.heappush(priority_queue,
                                  Bode(temp_state,
                                        curr_Bode,
                                        letter,
                                        curr_Bode.path_cost + 1,
                                        temp_state.heuristic1()))
                    explored_set.add(temp_state.__hash__())

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

        print("search unable to find a solution.")
        return


def AStar(search, state):

    if search == "tree":
        priority_queue = [Bode(state, None, None, 0, state.heuristic1())]
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            curr_Bode = heapq.heappop(priority_queue) # get next node in queue
            curr_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                if temp_state.agent_loc != curr_state.agent_loc: # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:
                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # add new state to priority queue
                    heapq.heappush(priority_queue,
                                   Bode(temp_state,
                                        curr_Bode,
                                        letter,
                                        curr_Bode.path_cost + 1,
                                        temp_state.heuristic1() +
                                        curr_Bode.path_cost + 1))

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

        print("search unable to find a solution.")
        return

    if search == "graph":
        priority_queue = [Bode(state, None, None, 0, state.heuristic1())]
        explored_set = {state.__hash__()}
        nodes_generated = 1
        curr_nodes_stored = 1
        max_nodes_stored = 1

        while True:
            curr_Bode = heapq.heappop(priority_queue) # get next node in queue
            curr_nodes_stored -= 1
            curr_state = curr_Bode.state

            for letter in "UDRL":
                temp_state = copy.deepcopy(curr_state)
                temp_state.move_agent(letter)

                if (temp_state.agent_loc != curr_state.agent_loc and
                    temp_state.__hash__() not in explored_set): # agent moved

                    # print(temp_state.__str__()) # print if agent moves

                    # upon finished state print total nodes generated,
                    # maximum nodes in frontier at any time, pathway by agent.
                    if temp_state.all_clean() == True:

                        print("nodes generated: ", nodes_generated)
                        print("max nodes stored: ", max_nodes_stored)

                        pathway = [letter]
                        parent = curr_Bode
                        while parent.action != None:
                            pathway.insert(0, parent.action)
                            parent = parent.parent
                        print("pathway taken by agent: ", pathway)
                        print("number of moves made: ", len(pathway))

                        return pathway

                    # add new state to priority queue and explored set
                    heapq.heappush(priority_queue,
                                  Bode(temp_state,
                                        curr_Bode,
                                        letter,
                                        curr_Bode.path_cost + 1,
                                        temp_state.heuristic1() + curr_Bode.path_cost + 1))
                    explored_set.add(temp_state.__hash__())

                    nodes_generated += 1 #tracking time complexity
                    curr_nodes_stored += 1 #tracking space complexity
                    if curr_nodes_stored > max_nodes_stored:
                        max_nodes_stored = curr_nodes_stored

        print("search unable to find a solution.")
        return


def search(algorithm, search, state):
    """ makes calling functions easier from command line """
    if algorithm == "ASTAR":
        return AStar(search, state)
    if algorithm == "GBFS":
        return GBFS(search, state)
    if algorithm == "IDS":
        return IDS(search, state)
    if algorithm == "DFS":
        return DFS(search, state)
    if algorithm == "BFS":
        return BFS(search, state)


def make_vacuum_environment(k):
    """ Creates a unique environment depending on value of k """
    if k == 0:
        """ O O O O O O O
            O A D D D D O
            O D O O O E O
            O D D D D E O
            O D D O E E O
            O D D D E D O
            O O O O O O O
            optimal solution: 20 moves """
        return VacuumEnvironment375(5, 5, (2, 2),
                                  [(1, 4), (2, 4), (3, 4), (3, 3), (4, 3)],
                                  [(1, 1), (1, 2), (1, 3), (3, 2)])
    if k == 1:
        """ O O O O O
            O D O D O
            O D D A O
            O D O D O
            O D D D O
            O D O D O
            O D D D O
            O O O O O
            optimal solution: 17 moves """
        return VacuumEnvironment375(6, 3, (1, 2),
                                  [],
                                  [(0, 1), (2, 1), (4, 1)])
    if k == 2:
        """ O O O O O O O O O
            O D O D D D O D O
            O D D D O E D D O
            O D O D D D O D O
            O D D E E O D D O
            O O O O D A O D O
            O E D D D D D D O
            O D D D O D E D O
            O O O O O O O O O
            optimal solution: 42 moves """
        return VacuumEnvironment375(7, 7, (4, 4),
                                  [(1, 4), (3, 2), (3, 3), (5, 0), (6, 5)],
                                  [(0, 1), (0, 5), (1, 3), (2, 1), (2, 5),
                                   (3, 4), (4, 0), (4, 1), (4, 2), (4, 5),
                                   (6, 3)])
    if k == 3:
        """ O O O O O O O O O O O
            O D D D D D D D D D O
            O D A D D D D D D D O
            O D D O D D D D D D O
            O D D D O D D D D D O
            O D D D D D D D D D O
            O O D O O O O O D O O
            O D D O D D D D D D D
            O D D D O D D D D D D
            O O O O O O O O O O O
            optimal solution: 72 moves (hand-checked) """
        return VacuumEnvironment375(8, 9, (1, 1),
                                  [],
                                  [(5, 0), (5, 2), (5, 3), (5, 4), (5, 5),
                                   (5, 6), (5, 8), (2, 2), (3, 3), (6, 2),
                                   (7, 3)])

    # return VacuumEnvironment375(k + 2, k + 2, (0, 0))



    raise ValueError("environment {} does not exist".format(k))


def main():
    environment = int(sys.argv[1]) # run search on environment specified
    algorithm = str(sys.argv[2]).upper() # BFS, DFS, IDS, BestFirst, aStar
    type = str(sys.argv[3]).lower() # graph or tree
    bool_visualize = int(sys.argv[4]) # 0 or 1

    # steps = []
    # for i in range(8):
    #     steps.append(search(algorithm, type, make_vacuum_environment(i)))
    # pd.DataFrame(steps).to_excel('temp.xlsx', header=False, index=False)
    # for i in range(4):
    #     search(algorithm, type, make_vacuum_environment(i))
    path = search(algorithm, type, make_vacuum_environment(environment))
    if bool_visualize == 0:
        return
    return animate_path_taken(make_vacuum_environment(environment), path)

if __name__ == "__main__":
    main()
