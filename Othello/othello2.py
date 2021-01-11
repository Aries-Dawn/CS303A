import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DEEP = 3
STEEP = 0
random.seed(0)
ALPHA = float('-Inf')
BETA = float('Inf')
BEGIN_TIME = 0
Vmap = np.array([
    [500, -250, 30, 30, 30, 30, -250, 500],
    [-250, -500, 20, 0, 0, 20, -500, -250],
    [30, 20, 30, 5, 5, 30, 20, 30],
    [30, 2, 5, 2, 2, 5, 2, 30],
    [30, 2, 5, 2, 2, 5, 2, 30],
    [30, 20, 30, 5, 5, 30, 20, 30],
    [-250, -500, 20, 2, 2, 20, -500, -250],
    [500, -250, 30, 30, 30, 30, -250, 500],
])


# Vmap = np.array([
#     [90, -60, 20, 30, 30, 20, -60, 90],
#     [-60, -250, 5, 5, 5, 5, -250, -60],
#     [20, 5, 10, 1, 1, 1, 5, 20],
#     [30, 5, 5, 1, 1, 1, 5, 30],
#     [30, 5, 5, 1, 1, 1, 5, 30],
#     [20, 5, 10, 1, 1, 1, 5, 20],
#     [-60, -250, 5, 5, 5, 5, -250, -60],
#     [90, -60, 20, 30, 30, 20, -60, 90]
# ])


# don't change the class name


class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        self.time_out = time_out
        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_list as your decision.
        self.candidate_list = [()]

    def go(self, chessboard):
        global STEEP, DEEP, BEGIN_TIME
        BEGIN_TIME = time.time()
        STEEP += 1
        if STEEP <= 2:
            DEEP = 2
        elif STEEP <= 55:
            DEEP = 3
        else:
            DEEP = 9

        self.candidate_list.clear()
        # ==================================================================
        self.candidate_list = self.valid_position(chessboard, self.color)
        self.move_bad(chessboard)
        self.move_corner()
        number, position = self.mini_max(chessboard, 0, self.color, ALPHA, BETA)
        self.update(position)
        self.move_star()
        self.stable_tran(chessboard)
        self.move_corner()

    def edge(self):
        edges = [(0, 2), (0, 3), (0, 4), (0, 5),
                 (7, 2), (7, 3), (7, 4), (7, 5),
                 (2, 0), (3, 0), (4, 0), (5, 0),
                 (2, 7), (3, 7), (4, 7), (5, 7),
                 ]
        random.seed(time.time())
        random.shuffle(edges)
        for point in edges:
            self.update(point)

    def fresh(self, chessboard, C_V_map):
        if chessboard[0][0] == self.color:
            C_V_map[0][1] = 300
            C_V_map[1][0] = 300
            C_V_map[1][1] = 100
        if chessboard[0][7] == self.color:
            C_V_map[0][6] = 300
            C_V_map[1][7] = 300
            C_V_map[1][6] = 100
        if chessboard[7][0] == self.color:
            C_V_map[6][0] = 300
            C_V_map[7][1] = 300
            C_V_map[6][1] = 100
        if chessboard[7][7] == self.color:
            C_V_map[7][6] = 300
            C_V_map[6][7] = 300
            C_V_map[6][6] = 100

    def stable_tran(self, chessboard):
        if chessboard[0][0] == self.color:
            self.update((1, 1))
            self.update((0, 1))
            self.update((1, 0))
        if chessboard[0][7] == self.color:
            self.update((1, 6))
            self.update((0, 6))
            self.update((1, 7))
        if chessboard[7][0] == self.color:
            self.update((6, 1))
            self.update((6, 0))
            self.update((7, 1))
        if chessboard[7][7] == self.color:
            self.update((6, 6))
            self.update((6, 7))
            self.update((7, 6))

    def update(self, point):
        if point in self.candidate_list:
            self.candidate_list.remove(point)
            self.candidate_list.append(point)

    def move_star(self):
        star = [(1, 1), (1, 6), (6, 1), (6, 6)]
        choose = len(self.candidate_list) - 1
        for i in range(len(self.candidate_list)):
            if self.candidate_list[choose] in star:
                self.candidate_list[choose], self.candidate_list[i] = self.candidate_list[i], self.candidate_list[
                    choose]
            if self.candidate_list[choose] in star:
                continue
            else:
                break

    def move_bad(self, board):
        bad = self.get_bad(board)
        choose = len(self.candidate_list) - 1
        for i in range(len(self.candidate_list)):
            if self.candidate_list[choose] in bad:
                self.candidate_list[choose], self.candidate_list[i] = self.candidate_list[i], self.candidate_list[
                    choose]
            if self.candidate_list[choose] in bad:
                continue
            else:
                break

    def get_bad(self, chessboard):

        bad = [(0, 1), (1, 0), (1, 1),
               (0, 6), (1, 7), (1, 6),
               (6, 0), (6, 1), (7, 1),
               (6, 6), (7, 6), (6, 7)]
        if chessboard[0][0] == self.color:
            bad.remove((1, 1))
            bad.remove((0, 1))
            bad.remove((1, 0))

        if chessboard[0][7] == self.color:
            bad.remove((0, 6))
            bad.remove((1, 6))
            bad.remove((1, 7))

        if chessboard[7][0] == self.color:
            bad.remove((6, 1))
            bad.remove((6, 0))
            bad.remove((7, 1))

        if chessboard[7][7] == self.color:
            bad.remove((6, 6))
            bad.remove((7, 6))
            bad.remove((6, 7))
        return bad

    def move_corner(self):
        corner = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for point in corner:
            self.update(point)

    def valid_position(self, chessboard, color):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        result = []
        for idx_temp in idx:
            judgement = self.judge(idx_temp[0], idx_temp[1], chessboard, color)
            if judgement:
                result.append((idx_temp[0], idx_temp[1]))
        random.seed(time.time())
        random.shuffle(result)
        return result

    def judge(self, x, y, chessboard, color):
        dirs = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        CURRENT_COLOR = color
        size = self.chessboard_size
        tag = False
        eat = 0
        for d in dirs:
            c_x = x + d[0]
            c_y = y + d[1]
            if 0 > c_x or c_x >= size or 0 > c_y or c_y >= size or chessboard[c_x][c_y] == COLOR_NONE or \
                    chessboard[c_x][c_y] == CURRENT_COLOR:
                continue
            else:
                temp_eat = 0
                while 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == -color:
                    c_x = c_x + d[0]
                    c_y = c_y + d[1]
                    temp_eat += 1
                if 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == CURRENT_COLOR:
                    eat += temp_eat
                    tag = True
        return tag

    def move(self, x, y, board, color):
        chessboard = board.copy()
        dirs = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        CURRENT_COLOR = color
        size = self.chessboard_size
        chessboard[x][y] = color
        eat = 0
        for d in dirs:
            c_x = x + d[0]
            c_y = y + d[1]
            if 0 > c_x or c_x >= size or 0 > c_y or c_y >= size or chessboard[c_x][c_y] == COLOR_NONE or \
                    chessboard[c_x][c_y] == CURRENT_COLOR:
                continue
            else:
                temp_eat = 0
                eat_pos = []
                while 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == -color:
                    c_x = c_x + d[0]
                    c_y = c_y + d[1]
                    eat_pos.append((c_x, c_y))
                    temp_eat += 1
                if 0 <= c_x < size and 0 <= c_y < size and chessboard[c_x][c_y] == CURRENT_COLOR:
                    eat += temp_eat
                    for c_x, c_y in eat_pos:
                        chessboard[c_x][c_y] = color
        return chessboard

    def mini_max(self, chessboard, deep, moving, alpha, beta):
        result = []
        c_time = time.time()
        m_droppable_list = self.valid_position(chessboard, moving)
        e_droppable_list = self.valid_position(chessboard, -moving)
        me = np.where(chessboard == self.color)
        me = list(zip(me[0], me[1]))
        enemy = np.where(chessboard == -self.color)
        enemy = list(zip(enemy[0], enemy[1]))
        if len(m_droppable_list) == 0 and len(e_droppable_list) == 0:
            return len(me) - len(enemy), result
        if deep == DEEP and c_time - BEGIN_TIME < 2.3:
            return self.evaluation(chessboard, self.color), result

        if moving == self.color:
            for drop in m_droppable_list:
                new_board = self.move(drop[0], drop[1], chessboard, moving)
                temp_val, temp_point = self.mini_max(new_board, deep + 1, -moving, alpha, beta)

                # print(temp_val, temp_point, deep)
                # print(new_board)
                if temp_val >= beta:
                    return temp_val, drop
                if temp_val > alpha:
                    alpha = temp_val
                    result = drop
            return alpha, result
        elif moving == -self.color:
            for drop in m_droppable_list:
                new_board = self.move(drop[0], drop[1], chessboard, moving)
                temp_val, temp_point = self.mini_max(new_board, deep + 1, -moving, alpha, beta)

                # print(temp_val, temp_point, deep)
                # print(new_board)
                if temp_val <= alpha:
                    return temp_val, drop
                if temp_val <= beta:
                    beta = temp_val
                    result = drop
            return beta, result

    def map_weight_sum(self, board, C_V_map):
        return sum(sum(board * C_V_map)) * self.color

    def get_moves(self, board, color):
        moves = self.valid_position(board, color)
        return len(moves)

    def calculate_stability(self, chessboard, color):
        stable = 0
        idx = np.where(chessboard == color)
        idx = list(zip(idx[0], idx[1]))
        for temp in idx:
            stable += self.stability(temp[0], temp[1], chessboard, color)
        return stable

    def stability(self, x, y, chessboard, color):
        direct = [(0, 1), (-1, 1), (-1, 0), (-1, -1)]
        size = self.chessboard_size
        tag = 0
        for d in direct:
            c_x = x
            c_y = y
            c_x2 = x
            c_y2 = y
            while 0 <= c_x < size and 0 <= c_y < size:
                if chessboard[c_x][c_y] == color:
                    c_x = c_x + d[0]
                    c_y = c_y + d[1]
                else:
                    break
            while 0 <= c_x2 < size and 0 <= c_y2 < size:
                if chessboard[c_x2][c_y2] == color:
                    c_x = c_x + d[0]
                    c_y = c_y + d[1]
                else:
                    break
            if (not (0 <= c_x < size and 0 <= c_y < size)) or (not (0 <= c_x2 < size and 0 <= c_y2 < size)):
                tag += 1

            else:
                if chessboard[c_x][c_y] == -color and chessboard[c_x2][c_y2] == -color:
                    tag += 1
        return tag

    # This using in find out how many stable point in chessboard of one player
    def get_stable(self, chessboard, color):
        stable = 0
        idx = np.where(chessboard == color)
        idx = list(zip(idx[0], idx[1]))
        for temp in idx:
            if self.check_stable(temp[0], temp[1], chessboard, color):
                stable += 1
        return stable

    def all_edge(self, chessboard):
        val = 0
        temp_val = 0
        x, y = 0, 0
        begin = False
        connected = True
        while y < 8 and (begin or connected):
            if begin:
                if chessboard[x][y] == self.color:
                    temp_val += 1
                if chessboard[x][y] == -self.color:
                    temp_val = 0
                    break

            else:
                if chessboard[x][y] == self.color:
                    begin = True
            y += 1
        val += temp_val

        temp_val = 0
        x, y = 0, 7
        begin = False
        connected = True
        while x < 8 and (begin or connected):
            if begin:
                if chessboard[x][y] == self.color:
                    temp_val += 1
                if chessboard[x][y] == -self.color:
                    temp_val = 0
                    break

            else:
                if chessboard[x][y] == self.color:
                    begin = True
            x += 1
        val += temp_val

        temp_val = 0
        x, y = 7, 7
        begin = False
        connected = True
        while y >= 0 and (begin or connected):
            if begin:
                if chessboard[x][y] == self.color:
                    temp_val += 1
                if chessboard[x][y] == -self.color:
                    temp_val = 0
                    break

            else:
                if chessboard[x][y] == self.color:
                    begin = True
            y -= 1
        val += temp_val

        temp_val = 0
        x, y = 7, 0
        begin = False
        connected = True
        while x >= 0 and (begin or connected):
            if begin:
                if chessboard[x][y] == self.color:
                    temp_val += 1
                if chessboard[x][y] == -self.color:
                    temp_val = 0
                    break

            else:
                if chessboard[x][y] == self.color:
                    begin = True
            x -= 1
        val += temp_val

        return val

    def check_stable(self, x, y, chessboard, color):
        direct = [(0, 1), (-1, 1), (-1, 0), (-1, -1)]
        size = self.chessboard_size
        tag = True
        for d in direct:
            c_x = x
            c_y = y
            d1 = True
            d2 = True
            fall = True
            while 0 <= c_x < size and 0 <= c_y < size:
                if chessboard[c_x][c_y] != color:
                    d1 = False
                if chessboard[c_x][c_y] == COLOR_NONE:
                    fall = False
                c_x = c_x + d[0]
                c_y = c_y + d[1]

            if not d1:
                while 0 <= c_x < size and 0 <= c_y < size:
                    if d2 and chessboard[c_x][c_y] != color:
                        d2 = False
                    if chessboard[c_x][c_y] == COLOR_NONE:
                        fall = False
                    c_x = c_x + d[0]
                    c_y = c_y + d[1]
            tag = d1 or d2 or fall
            if not tag:
                break

        return tag

    def evaluation(self, board, my_color):
        C_V_map = np.copy(Vmap)
        self.fresh(C_V_map, board)
        moves = self.get_moves(board, my_color)
        moves_ = self.get_moves(board, -my_color)
        # my_stable = self.get_stable(board, my_color)
        # enemy_stable = self.get_stable(board, -my_color)
        my_stability = self.calculate_stability(board, my_color)
        enemy_stability = self.calculate_stability(board, -my_color)
        matrix = self.map_weight_sum(C_V_map, board)
        my_point = 0
        enemy_point = 0
        # edge = self.all_edge(board)
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if board[i][j] == self.color:
                    my_point += 1
                elif board[i][j] == -self.color:
                    enemy_point += 1
        global STEEP
        if STEEP < 20:
            value = matrix \
                    + (moves - moves_) \
                    + 20 * (my_stability - enemy_stability)
        elif 24 < STEEP <= 44:
            value = matrix \
                    + 40 * (moves - moves_) \
                    + 20 * (my_stability - enemy_stability)
        # elif STEEP >= 40:
        #     value = matrix \
        #             + 20 * (moves - moves_) \
        #             + 20 * (my_stability - enemy_stability) \
        #             + 30 * (my_point - enemy_point)
        else:
            value = matrix \
                    + (moves - moves_) \
                    + 30 * (my_stability - enemy_stability)
        # if STEEP < 20:
        #     value = 10 * matrix \
        #             + 30 * (moves - moves_) \
        #             + 20 * (my_stable - enemy_stable) + 20 * (my_stability - enemy_stability)
        # elif 26 < STEEP < 40:
        #     value = 10 * matrix \
        #             + 20 * (moves - moves_) \
        #             + 40 * (my_stable - enemy_stable) + 40 * (my_stability - enemy_stability)
        # elif STEEP >= 40:
        #     value = 10 * matrix \
        #             + (moves - moves_) \
        #             + 30 * (my_stable - enemy_stable) + 20 * (my_stability - enemy_stability)\
        #             + 30 * (my_point - enemy_point)
        #
        # else:
        #     value = 10 * matrix \
        #             + (moves - moves_) \
        #             + 30 * (my_stable - enemy_stable) + 20 * (my_stability - enemy_stability)
        return int(value)
