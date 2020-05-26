#My Sudoku Solver

class Solution:

    def __init__(self):
        self.box_len  = 3
        self.grid_len = 9
        self.subbox   = [ [ [0]*10 for _ in range(self.box_len)] for _ in range(self.box_len)] # counter for subbox. size is 10: trade memory for readability and time
        self.row      = [ [0]*10 for _ in range(self.grid_len)]                                # counter for each row
        self.column   = [ [0]*10 for _ in range(self.grid_len)]                                # counter for each column
        self.route    = []
        self.board    = [[]]
        self.flag     = False

    def init(self, board):
        '''init subbox, row, column'''
        self.board = board
        for i in range(self.grid_len):
            for j in range(self.grid_len):
                try:
                    number = int(board[i][j])         # raise exception when "."
                    self.row[i][number]    = 1        # number is the index
                    self.column[j][number] = 1
                    out_i = i // self.box_len
                    out_j = j // self.box_len
                    self.subbox[out_i][out_j][number] = 1
                except:
                    pass

    def check(self, number, loc):
        '''check whether number is valid at loc'''
        i, j  = loc[0], loc[1]
        out_i = i // self.box_len
        out_j = j // self.box_len
        if self.subbox[out_i][out_j][number] == 1:  # step 1: check subbox
            return False
        if self.row[i][number] == 1:                # step 2: check row
            return False
        if self.column[j][number] == 1:             # step 3: check column
            return False
        return True

    def put(self, number, loc):
        '''put the number at loc'''
        i, j  = loc[0], loc[1]
        out_i = i // self.box_len
        out_j = j // self.box_len
        self.board[i][j] = str(number)
        self.subbox[out_i][out_j][number] = 1
        self.row[i][number] = 1
        self.column[j][number] = 1

    def unput(self, number, loc):
        '''remove the number at loc'''
        i, j = loc[0], loc[1]
        out_i = i // self.box_len
        out_j = j // self.box_len
        self.subbox[out_i][out_j][number] = 0
        self.row[i][number] = 0
        self.column[j][number] = 0        

    def backtrack(self, indx):
        if indx == len(self.route):
            self.flag = True                   # found the single unique solution!
            return
        loc = self.route[indx]
        for number in range(1, 10):
            if self.flag is True:
                return
            if self.check(number, loc) is True:
                self.put(number, loc)
                self.backtrack(indx + 1)
                self.unput(number, loc)

    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.init(board)
        self.route = []                                 # define a backtrack route (fill the subbox has priority)
        for out_i in range(self.box_len):               # index for the subbox
            for out_j in range(self.box_len):
                for in_i in range(self.box_len):        # index inside the subbox
                    for in_j in range(self.box_len):
                        i = out_i*self.box_len + in_i
                        j = out_j*self.box_len + in_j
                        if board[i][j] != '.':
                            continue
                        self.route.append((i, j))
        self.backtrack(0)                               # start at the zero-th index of the route
