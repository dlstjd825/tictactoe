# game.py
import numpy as np
from collections import deque

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.history = {1: deque(), 2: deque()}
        self.current_player = 1

    def reset(self):
        self.board.fill(0)
        self.history = {1: deque(), 2: deque()}
        self.current_player = 1
        return self.get_state()

    def get_state(self):
        return tuple(self.board.flatten())

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def step(self, action):
        i, j = action
        if self.board[i, j] != 0:
            return self.get_state(), -10, True

        if len(self.history[self.current_player]) >= 3:
            old_i, old_j = self.history[self.current_player].popleft()
            self.board[old_i, old_j] = 0

        self.board[i, j] = self.current_player
        self.history[self.current_player].append((i, j))

        done = self.check_winner(self.current_player)
        reward = 1 if done else 0
        self.current_player = 3 - self.current_player
        return self.get_state(), reward, done

    def check_winner(self, player):
        b = (self.board == player)
        for i in range(3):
            if all(b[i, :]) or all(b[:, i]):
                return True
        if b[0, 0] and b[1, 1] and b[2, 2]:
            return True
        if b[0, 2] and b[1, 1] and b[2, 0]:
            return True
        return False
    
    def get_winner(self):
        for player in [1, 2]:
            if self.check_winner(player):
                return player
        return 0  # 무승부 or 아직 진행 중

