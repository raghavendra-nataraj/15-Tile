from copy import deepcopy
import sys
class State():
    def __init__(self,st,hs,path):
	self.st = st
	self.hs = hs
	self.path = path
	
fringe = []
mem = []
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
    return sum+len(stat.path)	
	
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
    if state in mem:
        return False
    else:
        mem.append(state)
        return True

def is_goal(state):
    return all( [state[i]==i+1 for i in range(0,len(state)-1)])

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
     return state.hs

# Main code starts
iboard = []
for in_file in open(sys.argv[1]).read().split('\n'):
    iboard.extend([int(n) for n in in_file.split( )])
pBoard(iboard)
state = State(iboard,0,[])
state.hs = heuristic(state)
result = solve(state)
pBoard(result.st)
print result.path
