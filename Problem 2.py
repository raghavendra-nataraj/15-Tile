import copy
debug = 0
visited_boards = set()

class succ_board:
    # Heuristic function that calculates the number of misplaced tiles
    def calc_heuristic(self):
        self.heuristic = 0
        for r in range(0, 4):
            for c in range(0, 4):
                if r == 3 and c == 3:
                    if self.board[r][c] != 0:
                        if debug == 1:
                            print "Reached this cell"
                        self.heuristic += 1
                else:
                    if self.board[r][c] != ((c + 1) + (4 * r)):
                        self.heuristic += 1

    def __init__(self, in_board, blankrow, blankcol):
        self.board = in_board
        self.br = blankrow
        self.bc = blankcol
        self.calc_heuristic()

    def __eq__(self, cloneboard):
        """Override the default Equals behavior"""
        if isinstance(cloneboard, self.__class__):
            return str(self.board) == str(cloneboard.board)
        return False

    def __ne__(self, cloneboard):
        """Define a non-equality test"""
        if isinstance(cloneboard, self.__class__):
            return not self.__eq__(cloneboard)
        return False

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(str(self.board))))

    def __str__(self):
        return str(self.board).replace("], [", "],\n [") + "\n--------------\n"

    def __repr__(self):
        return self.__str__()

    def clone_board(self, new_br, new_bc):
        in_board = copy.deepcopy(self.board)
        in_board[self.br][self.bc], in_board[new_br][new_bc] = in_board[new_br][new_bc], in_board[self.br][self.bc]
        new_board = succ_board(in_board, new_br, new_bc)
        if not visited_boards.__contains__(new_board):
            if debug == 1:
                print "Clone created: \n" + print_board(new_board.board)
            return new_board

    def move_up(self):
        return self.clone_board((self.br - 1)%4, self.bc)

    def move_down(self):
        return self.clone_board((self.br + 1)%4, self.bc)

    def move_left(self):
        return self.clone_board(self.br, (self.bc - 1)%4)

    def move_right(self):
        return self.clone_board(self.br, (self.bc + 1)%4)

    # Code for moving only the corner tiles
    # def move_edge(self):
    #     if self.br % 3 == 0 and self.bc % 3 == 0:
    #         return self.clone_board(abs(self.br - 3), self.bc), self.clone_board(self.br, abs(self.bc - 3))

# Get the position of the empty tile, i.e., number 0
def get_empty_tile(board):
    for row in range(0, 4):
        for col in range(0, 4):
            if board[row][col] == 0:
                return row, col

def print_board(board):
    return str(board).replace("], [", "],\n [")

# Get list of successors of given board state
def successors(curr_board):
    if debug == 1:
        print "In successors:"
    succ_list = []

    if debug == 1:
        print "In move up"
    up_board = curr_board.move_up()
    if up_board:
        succ_list.append(up_board)

    if debug == 1:
        print "In move down"
    down_board = curr_board.move_down()
    if down_board:
        succ_list.append(down_board)

    if debug == 1:
        print "In move left"
    left_board = curr_board.move_left()
    if left_board:
        succ_list.append(left_board)

    if debug == 1:
        print "In move right"
    right_board = curr_board.move_right()
    if right_board:
        succ_list.append(right_board)

    # if debug == 1:
    #     print "In move edge"
    # if (curr_board.move_edge()):
    #     edge_board1, edge_board2 = curr_board.move_edge()
    #     if edge_board1:
    #         succ_list.append(edge_board1)
    #     if edge_board2:
    #         succ_list.append(edge_board2)

    if debug == 1:
        print "End of succ function"
        # print "Original Board: \n" + print_board(curr_board.board)
    if debug == 1:
        print "Length of successor list: " + str(len(succ_list))
    if len(succ_list) > 0:
        return sorted(succ_list, key=lambda x: x.heuristic, reverse=True)
    else:
        return succ_list

# Check for the goal state
def is_goal(board):
    if debug == 1:
        print "In is goal"
    if board.heuristic == 0:
        return 1
    else:
        return 0

# Solve 15-puzzle!
def solve(initial_stage):
    if debug == 1:
        print "In solve"
    fringe = [initial_stage]
    while len(fringe) > 0:
        x = fringe.pop()
        visited_boards.add(x)
        if debug == 1:
            print "Fringe board before is goal: \n" + print_board(x.board)
        # check if is_goal(x)
        if is_goal(x):
            return x.board
        if debug == 1:
            print "Fringe board: \n" + print_board(x.board)
            print "Heuristic value for popped board:" + str(x.heuristic)
        for s in successors(x):
            if s:
                if debug == 1:
                    print "on next iteration \n" + print_board(s.board)
                    print "Blankrow: " + str(s.br)
                    print "Blankcol: " + str(s.bc)
                    print "heuristic value of this board:" + str(s.heuristic)
                fringe.append(s)
    return False

# Main code starts
initial_board = list(list(int(l) for l in in_file.split(' ') if l) for in_file in open("15-puzzle.txt").read().split('\n'))
# initial_board = list(list(int(l) for l in in_file.split(' ') if l) for in_file in open("15-puzzle_test2.txt").read().split('\n'))
row, col = get_empty_tile(initial_board)
print "Initial board: \n" + print_board(initial_board)
if debug == 1:
    print row, col

start_board = succ_board(initial_board, row, col)
if debug == 1:
    print "Heuristic value for start board = " + str(start_board.heuristic)

solution = solve(start_board)
print "Goal State Reached: \n" + print_board(solution) if solution else "Sorry, no solution found. :("
if debug == 1:
    print "Visited Boards: \n" + str(visited_boards)
print "End of program"