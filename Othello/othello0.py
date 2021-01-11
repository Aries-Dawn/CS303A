import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name


class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time
        # must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_list as your decision.
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for idx_temp in idx:
            judgement = self.judge(idx_temp[0], idx_temp[1], chessboard)
            if judgement:
                self.candidate_list.append((idx_temp[0], idx_temp[1]))
        random.seed(5)
        random.shuffle(self.candidate_list)

    def dead(self, x, y):
        if ((x == 1 and (y == 1 or y == self.chessboard_size - 2)) or
                (x == self.chessboard_size - 2 and (y == 1 or y == self.chessboard_size - 2))):
            return True

    def has_corner(self, source):
        result = []
        tag = False
        for idx in source:
            if ((idx[0] == 0 and (idx[1] == 0 or idx[1] == self.chessboard_size - 1)) or
                    (idx[0] == self.chessboard_size - 1 and (idx[1] == 0 or idx[1] == self.chessboard_size - 1))):
                result.append(idx)
                tag = True
        # result = sorted(result, reverse=True)
        return tag, result

    def judge(self, x, y, chessboard):
        dirs = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        CURRENT_COLOR = self.color
        size = self.chessboard_size
        tag = False
        eat = 0
        for dir in dirs:
            c_x = x + dir[0]
            c_y = y + dir[1]
            if 0 > c_x or c_x >= size or 0 > c_y or c_y >= size or chessboard[c_x][c_y] == COLOR_NONE or \
                    chessboard[c_x][c_y] == CURRENT_COLOR:
                continue
            else:
                temp_eat = 0
                while 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == -self.color:
                    c_x = c_x + dir[0]
                    c_y = c_y + dir[1]
                    temp_eat += 1
                if 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == CURRENT_COLOR:
                    eat += temp_eat
                    tag = True
        return tag

    # def minimax(self, chessboard):

    # ==============Find new pos========================================
    # Make sure that the position of your decision in chess board is empty.
    # If not, the system will return error.
    # Add your decision into candidate_list, Records the chess board
    # You need add all the positions which is valid
    # candidate_list example: [(3,3),(4,4)]
    # You need append your decision at the end of the candidate_list,
    # we will choose the last element of the candidate_list as the position you choose
    # If there is no valid position, you must return a empty list.
