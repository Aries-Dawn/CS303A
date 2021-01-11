from othello2 import AI
import numpy as np

chessboard = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, -1, 0, 0, 0],
              [0, 0, 0, -1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]
print(chessboard)
chessboard = np.array(chessboard)
ai = AI(8, 1, 5)
# ai.go(chessboard)
print(ai.valid_position(chessboard,-1))
print(len(ai.candidate_list))
# print(sum(sum(chessborad * Vmap)) * 1)
