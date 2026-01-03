# Jurgis Vass jtv34

import random
import sys
from queue import Queue
from queue import PriorityQueue
import math

eightPuzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def cmd(cmdString: str):
    cmdString.strip()
    if cmdString.startswith("#") or cmdString.startswith("//") or cmdString == "": # skip over comments and blank lines
        return None
    (fun, sep, input) = cmdString.partition(" ")
    match fun:
        case "setState":
            setState(input)
        case "printState":
            printState()
        case "move":
            move(input)
        case "scrambleState": # scramble param must be a number
            if input.isdecimal():
                scrambleState(int(input))
            else: 
                print(f"Error: invalid command: {input}")
        case "setSeed": # turn seed into number or leave as string
            if input.isdecimal():
                setSeed(int(input))
            else:
                set(input)
        case "solve": # another match statement for dfs or bfs
            if input.strip() == "":
                print(f"Error: invalid command: {fun}")
                return None
            input = input.split(" ") # much parsing for arguments
            match input[0]:
                case "DFS":
                    if len(input) == 1:
                        dfs()
                    elif len(input) == 2 and input[1].startswith("maxnodes="):
                        mn = int(input[1].replace("maxnodes=", ""))
                        dfs(mn)
                    elif input[1].startswith("maxnodes=") and input[2].startswith("depthlimit="):
                        mn = int(input[1].replace("maxnodes=", ""))
                        dl = int(input[2].replace("depthlimit=", ""))
                        dfs(mn, dl)
                    else:
                        del input[0]
                        print(f"Error: invalid command: {" ".join(input)}")
                case "BFS": # more annoying parsing
                    if len(input) == 1:
                        bfs()
                    elif input[1].startswith("maxnodes="):
                        mn = int(input[1].replace("maxnodes=", ""))
                        bfs(mn)
                    else:
                        del input[0]
                        print(f"Error: invalid command: {" ".join(input)}")
                case "A*":
                    if len(input) == 1:
                        print("Error: invalid command: A*")
                    elif len(input) == 2 and (input[1] == "h1" or input[1] == "h2"):
                        aStar(input[1])
                    elif len(input) == 3 and input[2].startswith("maxnodes=") and (input[1] == "h1" or input[1] == "h2"):
                        mn = int(input[2].replace("maxnodes=", ""))
                        aStar(input[1], mn)
                    else:
                        print(f"Error: invalid command: {" ".join(input)}")
                case _:
                    print(f"Error: invalid command: {input[0]}")
        case "heuristic":
            if input == "h1" or input == "h2":
                print(heuristic(eightPuzzle.copy(), input)) # defaults to the current eightpuzzle state
            else:
                print(f"Error: invalid command: {input}")
        case "EBF":
            if input.strip() == "":
                print(f"Error: invalid command: {fun}")
                return None
            input = input.split()
            print(input[0])
            if len(input) != 2:
                print(f"Error: invalid command: {" ".join(input)}")
                return None
            elif input[0].isdecimal() and input[1].isdecimal():
                print(ebf(int(input[0]), int(input[1])))
            else:
                print(f"Error: invalid command: {" ".join(input)}")
                return None
        case _: 
            print(f"Error: invalid command: {fun}")
     
def setState(puzzleString: str):
    global eightPuzzle
    if len(puzzleString) > 17 or len(puzzleString) < 17: # must be of form "x x x x x x x x x" where x is a digit
        print("Error: invalid puzzle state")
        return None
    elif not puzzleString.replace(" ", "").isdecimal():
        print("Error: invalid puzzle state")
        return None
    puzzleNums = list(map(int, puzzleString.split(" "))) # parse and convert to integers
    if sorted(puzzleNums) == [0, 1, 2, 3, 4, 5, 6, 7, 8]: # all digits must be different
        eightPuzzle = puzzleNums
    else:
        print("Error: invalid puzzle state")

def printState():
    p = "".join(map(str, eightPuzzle)).replace("0", " ") # convert to string and replace 0 with space
    print(f"""{p[0]}{p[1]}{p[2]}
{p[3]}{p[4]}{p[5]}
{p[6]}{p[7]}{p[8]}""")

def move(dir: str):
    blank = eightPuzzle.index(0)
    match dir: # swap blank and tile based on index arithmetic
        case "up":
            if blank < 3:
                print("Error: invalid move")
            else:
                eightPuzzle[blank], eightPuzzle[blank - 3] = eightPuzzle[blank - 3], eightPuzzle[blank]
        case "down": 
            if blank > 5:
                print("Error: invalid move")
            else:
                eightPuzzle[blank], eightPuzzle[blank + 3] = eightPuzzle[blank + 3], eightPuzzle[blank]
        case "left": 
            if blank % 3 == 0:
                print("Error: invalid move")
            else:
                eightPuzzle[blank], eightPuzzle[blank - 1] = eightPuzzle[blank - 1], eightPuzzle[blank]
        case "right": 
            if blank % 3 == 2:
                print(f"Error: invalid command: {dir}")
            else:
                eightPuzzle[blank], eightPuzzle[blank + 1] = eightPuzzle[blank + 1], eightPuzzle[blank]
        case _:
            print("Error: invalid move")

def scrambleState(n: int):
    setState("0 1 2 3 4 5 6 7 8") # initialize to solved state
    dirs = ["up", "down", "left", "right"]
    for i in range(n):
        blank = eightPuzzle.index(0)
        tempDirs = dirs[:] # remove invalid moves
        if blank < 3:
            tempDirs.remove("up")
        if blank > 5:
            tempDirs.remove("down")
        if blank % 3 == 0:
            tempDirs.remove("left")
        if blank % 3 == 2:
            tempDirs.remove("right")
        ranDir = random.choice(tempDirs)
        move(ranDir)

def setSeed(s: int):
    random.seed(s)

def simulateMove(node: tuple[int], move: str) -> list[int] | None: # helper function to check the next state without modifying eightPuzzle
    state = list(node)
    b = state.index(0)
    match move:
        case "up":
            if b < 3:
                return None
            state[b], state[b - 3] = state[b - 3], state[b]
            return state
        case "down":
            if b > 5:
                return None
            state[b], state[b + 3] = state[b + 3], state[b]
            return state
        case "left":
            if b % 3 == 0:
                return None
            state[b], state[b - 1] = state[b - 1], state[b]
            return state
        case "right":
            if b % 3 == 2:
                return None
            state[b], state[b + 1] = state[b + 1], state[b]
            return state

def dfs(maxNodes = 1000, depthLimit = 31):
    global eightPuzzle
    solved = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    foundNodes = {} # remember visited nodes in a dictionary
    nodes = 1 # counts nodes visited
    stack = [(tuple(eightPuzzle.copy()), "start")] 
    while stack:
        node = stack.pop()
        if node[0] in foundNodes:
            continue
        if node[1] == "up": # this part get's the parent node's move path and adds the whole new path and state to the dictionary
            temp = foundNodes.get(tuple(simulateMove(node[0], "down"))).copy()
            temp.append("up")
            foundNodes.update({node[0]: temp})
        elif node[1] == "down":
            temp = foundNodes.get(tuple(simulateMove(node[0], "up"))).copy()
            temp.append("down")
            foundNodes.update({node[0]: temp})
        elif node[1] == "left":
            temp = foundNodes.get(tuple(simulateMove(node[0], "right"))).copy()
            temp.append("left")
            foundNodes.update({node[0]: temp})
        elif node[1] == "right":
            temp = foundNodes.get(tuple(simulateMove(node[0], "left"))).copy()
            temp.append("right")
            foundNodes.update({node[0]: temp})
        else: # start node
            foundNodes.update({node[0]: []})
        if node[0] == solved: # if solution has been found print everything
            print(f"Nodes created during search: {nodes}")
            print(f"Solution length: {len(foundNodes.get(node[0]))}")
            print("Move sequence:")
            for m in foundNodes.get(node[0]):
                print(f"move {m}")
            eightPuzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            return None
        if nodes >= maxNodes: # too many nodes and no solution yet
            print(f"Error: maxnodes limit ({maxNodes}) reached")
            return None
        for next in ["down", "up", "right", "left"]: # putting new states and (valid) moves on the stack
            # checking for valid moves, non visited nodes, and valid depth
            if simulateMove(node[0], next) != None and not tuple(simulateMove(node[0], next)) in foundNodes and len(foundNodes.get(node[0])) - 1 < depthLimit:
                stack.append((tuple(simulateMove(node[0], next)), next))
                nodes += 1
    print("Error: no solution given depth limit")

def bfs(maxNodes = 1000): # basically the same as dfs but with queue
    global eightPuzzle
    solved = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    foundNodes = {} # dictionary
    nodes = 1
    queue = Queue()
    queue.put((tuple(eightPuzzle.copy()), "start"))
    while queue:
        node = queue.get()
        if node[0] in foundNodes:
            continue
        if node[1] == "up": # this part get's the parent node's move path and adds the whole new path and state to the dictionary
            temp = foundNodes.get(tuple(simulateMove(node[0], "down"))).copy()
            temp.append("up")
            foundNodes.update({node[0]: temp})
        elif node[1] == "down":
            temp = foundNodes.get(tuple(simulateMove(node[0], "up"))).copy()
            temp.append("down")
            foundNodes.update({node[0]: temp})
        elif node[1] == "left":
            temp = foundNodes.get(tuple(simulateMove(node[0], "right"))).copy()
            temp.append("left")
            foundNodes.update({node[0]: temp})
        elif node[1] == "right":
            temp = foundNodes.get(tuple(simulateMove(node[0], "left"))).copy()
            temp.append("right")
            foundNodes.update({node[0]: temp})
        else: # start node
            foundNodes.update({node[0]: []})
        if node[0] == solved: # if solution has been found print everything
            print(f"Nodes created during search: {nodes}")
            print(f"Solution length: {len(foundNodes.get(node[0]))}")
            print("Move sequence:")
            for m in foundNodes.get(node[0]):
                print(f"move {m}")
            eightPuzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            return None
        if nodes >= maxNodes: # too many nodes and no solution yet
            print(f"Error: maxnodes limit ({maxNodes}) reached")
            return None
        for next in ["down", "up", "right", "left"]: # putting new states and (valid) put in the queue
            # checking for valid moves and non visited nodes
            if simulateMove(node[0], next) != None and not tuple(simulateMove(node[0], next)) in foundNodes:
                queue.put((tuple(simulateMove(node[0], next)), next))
                nodes += 1

def heuristic(state, h: str) -> int: # computes either hueristic based on passed in string
    match h:
        case "h1": # this one is easy
            count = 0;
            for i in range(0, 9):
                if state[i] != i and state[i] != 0:
                    count += 1
            return count
        case "h2": # this one is more complicated, using division by 3 with remainder to find the taxicab distance for each number except 0
            count = 0
            for i in range(0, 9):
                if state[i] != 0:
                    count += abs((state[i] % 3) - (i % 3)) + abs((state[i] // 3) - (i // 3))
            return count
        case _: # if for whatever reason the matching fails
            print(f"Error: invalid command: {h}")
            return None

def aStar(h: str, maxNodes = 1000): # also similar implimentation to bfs and dfs but with priority queue
    global eightPuzzle
    solved = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    foundNodes = {}
    nodes = 1
    pqueue = PriorityQueue() # priority queue based on lowest f(n) value
    pqueue.put((0, (tuple(eightPuzzle.copy()), "start"))) # priority 0 since it'll be popped imediately
    while pqueue:
        pnode = pqueue.get()
        node = pnode[1] # ignore the first part of tupe which is priority number
        if node[0] in foundNodes: # skip over already found nodes
            continue
        if node[1] == "up": # this part get's the parent node's move path and adds the whole new path and state to the dictionary
            temp = foundNodes.get(tuple(simulateMove(node[0], "down"))).copy()
            temp.append("up")
            foundNodes.update({node[0]: temp})
        elif node[1] == "down":
            temp = foundNodes.get(tuple(simulateMove(node[0], "up"))).copy()
            temp.append("down")
            foundNodes.update({node[0]: temp})
        elif node[1] == "left":
            temp = foundNodes.get(tuple(simulateMove(node[0], "right"))).copy()
            temp.append("left")
            foundNodes.update({node[0]: temp})
        elif node[1] == "right":
            temp = foundNodes.get(tuple(simulateMove(node[0], "left"))).copy()
            temp.append("right")
            foundNodes.update({node[0]: temp})
        else: # start node
            foundNodes.update({node[0]: []})
        if node[0] == solved: # if solution has been found print everything
            print(f"Nodes created during search: {nodes}")
            print(f"Solution length: {len(foundNodes.get(node[0]))}")
            print("Move sequence:")
            for m in foundNodes.get(node[0]):
                print(f"move {m}")
            eightPuzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            return None
        if nodes >= maxNodes: # too many nodes and no solution yet
            print(f"Error: maxnodes limit ({maxNodes}) reached")
            return None
        for next in ["down", "up", "left", "right"]:
            # checking for valid moves and non visited nodes
            if simulateMove(node[0], next) != None and not tuple(simulateMove(node[0], next)) in foundNodes:
                # priority heuristic calculation stuff, I usually put this all on 1 line but it is quite long
                f = len(foundNodes.get(node[0])) + 1 + heuristic(simulateMove(node[0], next), h) # +1 since our next checking node won't be stored yet
                pqueue.put((f, (tuple(simulateMove(node[0], next)), next)))
                nodes += 1

# effective branching factor
def ebf(n: int, d: int) -> float:
    # this will use binary search
    lb = 0
    ub = 10
    b = 1
    s = sum([pow(b, i) for i in range(1, d + 1)])
    while not math.isclose(n, s):
        if n > s: # b is too small
            lb = b
            b = (ub + b) / 2
        else: # b too large
            ub = b
            b = (lb + b) / 2
        s = sum([pow(b, i) for i in range(1, d + 1)])
    return b

def cmdFile(file: str):
    content = open(file, "r") # open file and parse
    for line in content:
        line = line.rstrip()
        print(line)
        cmd(line)
    content.close()


if len(sys.argv) == 1: # running commands in terminal
    quit = False
    while not quit:
        arg = input("|>")
        if arg == "quit":
            quit = True
        else:
            cmd(arg)
else: # running commands from file
    cmdFile(sys.argv[1]) 