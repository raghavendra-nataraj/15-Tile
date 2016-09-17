debug = 0

def is_goal(board):
    for row in range(0,4):
        for col in range(0,4):
            if debug == 1:
                print initial_board[row][col]
                print ((col + 1) + (4 * row))
            if row == 3 and col == 3 and initial_board[row][col] == 0:
                if debug == 1:
                    print "Reached this cell"
                return "goal state"
            else:
                if debug == 1:
                    print "In else"
                    print initial_board[row][col]
                    print ((col + 1) + (4 * row))
                if initial_board[row][col] != ((col + 1) + (4 * row)):
                    return "Not the goal state"

initial_board = list(list(int(l) for l in in_file.split(' ') if l) for in_file in open("15-puzzle.txt").read().split('\n'))
#initial_board = list(list(int(l) for l in in_file.split(' ') if l) for in_file in open("goal.txt").read().split('\n'))
print str(initial_board).replace("], [", "],\n [")
print is_goal(initial_board)