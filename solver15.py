#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Abstraction for problem 2:

a. Valid States, S = Any arrangement of 15 numbered tiles and an empty tile on the 4*4 board
d. Goal state, G = {S | S belongs to the set of valid states where all tiles are in order (increasing order from 1 to 15) and the empty tile (0th tile) is at the bottom right corner of the 4*4 board}
c. Initial state, S0 = 15 numbered tiles and an empty tile placed randomly on the 4*4 board
d. Successor function, Succ(S) = {S’ | S’ is list of states generated by sliding tile left, right, up or down and states generated by sliding the tile on the opposite side of the board only when the empty tile is on the edge of the 4*4 board}
e. Cost Function = Number of moves performed for reaching the goal state
f. Heuristic function defined: Sum of Manhattan distance between the tile positions in the current state and tile positions in the goal state.
  The Manhattan distance formula has been modified to account for the additional move allowed when the tile is on the edge of the board.
  The Manhattan distance gives the minimum number of moves required to move a given tile from it's current position to the goal position as it counts only the current tiles' moves, ignoring the other tiles that may get affected in this process. Hence it never underestimates the goal and is thus an admissible heuristic function.

How does the algorithm work?
The algorithm starts with the input board and includes it in the fringe. It then checks if it is the goal state. If yes, the program stops and prints the moves made. If the goal state is not reached, it then generates its successors based on the allowed moves of the empty tile. While generating the successors, it checks if any of the states have already been visited. If yes, it ignores that successor and does not append it to the list of successors. Once the successors are generated, the algorithm selects the most promising state (successor board) by comparing the sum of the cost and heuristic value which are defined as below:
Cost: Number of boards visited (or explored) to reach the current board configuration from the initial configuration (start board)
Heuristic value: Sum of Manhattan distance between tiles in current board and tiles in goal board
The algorithm selects the successor with the least value for the sum of the above cost and heuristic value. In this way, the algorithm keeps on exploring states until the goal state is reached.

The Heuristic function used and the design decisions made:
We initially used  Misplaced tiles as the heuristic function but it was taking a long time to get to the result.
We then changed the heuristic to Manhattan distance(changed to adopt the new variation) the program and it was returning results faster.
However the number of moves was quite high. So we introduced an additional heuristics to keep track of the length of path taken so far.
This made it little slow compared to earlier result because it would have to traverse more successors but it returned the results faster and with minimal number of moves.

The Cost of path traversed till current node is making the search slower(more like bfs) but it returns the shortest solution.
If just the heuristic is used then we get the solution very fast but however it is not the shortest solution.
So, we have introduced a factor called calibration factor which signifies the weightage of cost travelled so far.
Increasing the calibration factor will increase the time required to search and decrease the number of moves made.
Decreasing the value of calibration factor will decrease the time but it will have more moves.
We have made the factor as 0.9 which has tolerable time and the number of moves were shortest for all test cases we tested it for.
Calibration factor varies from 0.1 to 1.0.

Testcases : Obtained from the below link "http://codegolf.stackexchange.com/questions/6884/solve-the-15-puzzle-the-tile-sliding-puzzle"

'''

from copy import deepcopy
import sys
class State():
    def __init__(self,st,hs,path):
	self.st = st
	self.hs = hs
	self.path = path
	
fringe = []
mem = []
myGoal = range(1,16)
calibrationFactor = 0.9
def pBoard(state):
    board =  [ state[i*4:i*4+4] for i in range(0,4)]
    for i in board:
        print i
    print "\n"
    return board

def heuristic(stat):
    sum=0
    state = stat.st
    for i in state:
	index = state.index(i)
	inx = i-1
	if index != inx and i!=0:
		drow = abs(index/4-inx/4)
		dcol = abs(index%4-inx%4)
		row = min(drow,4-drow)
		col = min(dcol,4-dcol)
		sum=sum+(row+col)
    return sum
	
def addState(state,cPos,nPos):
    st =  deepcopy(state)
    nIndex = (nPos[0]%4)*4+(nPos[1]%4)
    temp = st[cPos]
    st[cPos] = st[nIndex]
    st[nIndex] = temp
    return st

def addPath(path,idx):
    dirc = ["U","D","L","R"]
    npath = path[:]
    npath.append(dirc[idx])
    return npath

def Successors(state):
    index = state.st.index(0)
    row = index/4
    col = index%4
    succ = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
    return [State(addState(state.st,index,pos),0,addPath(state.path,idx)) for idx,pos in enumerate(succ)]

def notExist(state):
    global mem
    if state in mem:
        return False
    else:
        mem.append(state)
        return True

def is_goal(state):
    #return all( [state[i]==i+1 for i in range(0,len(state)-1)])
    return state[0:15]== myGoal

# Solve 15-puzzle!
def solve(initial_stage):
    global fringe
    fringe.append(initial_stage)
    while len(fringe)>0:
        for state in Successors(fringe.pop()):
            if is_goal(state.st):
                return state
            if notExist(state.st):
                state.hs = heuristic(state)	
                fringe.append(state)
		fringe = sorted(fringe,key=getkey,reverse=True)
    return False

def getkey(state):
     return state.hs + len(state.path) * calibrationFactor

def isSolvable(st):
    row = st.index(0)/4
    st.remove(0)
    count=0
    return len([rest for idx,i in enumerate(st) for rest in st[idx+1:] if i>rest])+row+1

# Main code starts
iboard = []
for in_file in open(sys.argv[1]).read().split('\n'):
    iboard.extend([int(n) for n in in_file.split( )])
pBoard(iboard)
mem.append(iboard)
state = State(iboard,0,[])
state.hs = heuristic(state)
canSolve = isSolvable(state.st[:])
if canSolve%2==0:
    result =  solve(state)
    pBoard(result.st)
    print " ".join(s for s in result.path)
else:
    print "\nNot Solvable:-(\n"


