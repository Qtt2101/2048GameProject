import random
from copy import deepcopy
import numpy as np
GRID_SIZE=4
ACTION_DICT = {0: 'w', 1: 's', 2: 'a', 3: 'd'}
class Game2048:
    def __init__(self):
        # Khởi tạo trạng thái ban đầu
        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int32)
        self.score = 0
        self.done = False
        self.win = False
        
    # --- Hàm Hỗ trợ (Chuyển đổi thành phương thức) ---
    def _new_pieces(self, board):
        # Logic newpieces của bạn, nhưng dùng self.board
        empt = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == 0:
                    empt.append((i, j))
        if not empt:
            return board
        
        x, y = random.choice(empt)
        board[x][y] = 4 if random.randint(1, 10) == 1 else 2
        return board

    def _check_game_over(self):
        # Logic check_game_over của bạn
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == 0:
                    return False
                if c < GRID_SIZE - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return False
                if r < GRID_SIZE - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return False
        return True

    def _compress(self, a): # Dùng list như logic gốc của bạn
        sub=[0,0,0,0]
        i=0
        for x in a:
            if (x!=0):
                sub[i]=x
                i+=1
        return sub

    def _merge(self, a):
        score_gain = 0
        for i in range(3):
            if a[i] == a[i + 1]:
                a[i] = a[i] * 2
                score_gain += a[i]
                a[i + 1] = 0
        return self._compress(a), score_gain

    def _combin(self, a):
        compressed = self._compress(a)
        merged, score_gain = self._merge(compressed)
        return merged, score_gain

    def _reverse(self, board):
        return [row[::-1] for row in board]

    def _transpose(self, board):
        return [list(row) for row in zip(*board)]

    def _update_board(self, board, key):
        # Chuyển đổi board sang list trước khi xử lý nếu cần
        list_board = [list(row) for row in board]
        new_board_list = []
        total_score = 0
        
        # [PHẦN NÀY LÀ LOGIC update_board của bạn]
        # ... (Tương tự logic update_board của bạn, nhưng gọi _combin, _reverse, _transpose)
        
        # Sau khi xử lý xong list_board, chuyển lại thành numpy array
        # Ví dụ cho key='a':
        if key == 'a':
             for row in list_board:
                 new_row, gain = self._combin(row)
                 new_board_list.append(new_row)
                 total_score += gain
             return np.array(new_board_list), total_score

        if key== 'd':
            temp_board = self._reverse(list_board)
            for row in temp_board:
                new_row, gain =self._combin(row)
                new_board_list.append(new_row)
                total_score += gain
            return np.array(new_board_list), total_score
        if key == 'w':
            temp_board=self._transpose(list_board)
            for row in temp_board:
                new_row, gain= self._combin(list_board)
                new_board_list.append(new_row)
                total_score+=gain
            return np.array(new_board_list), total_score
        if key == 's':
            temp_board=self._reverse(self._transpose(list_board))
            for row in temp_board:
                new_row, gain=self._combin(list_board)
                new_board_list.append(new_row)
                total_score+= gain
            return np.array(new_board_list), total_score
        return board, 0 

   

    def reset(self):
        """Khởi động lại game, trả về trạng thái NumPy array."""
        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int32)
        self.score = 0
        self.done = False
        self.win = False
        self.board = self._new_pieces(self.board)
        self.board = self._new_pieces(self.board)
        return self.board

    def step(self, action_int):
        """
        Thực hiện bước chơi và trả về S', R, D.
        action_int: 0, 1, 2, 3
        """
        # 1. Chuyển đổi số nguyên sang ký tự ('w', 'a', 's', 'd')
        action_char = ACTION_DICT.get(action_int)
        if not action_char:
             raise ValueError("Hành động không hợp lệ!")
             
        old_board = self.board.copy()

        # 2. Cập nhật bảng và tính điểm
        new_board_np, score_gain = self._update_board(self.board, action_char)
        
        reward = score_gain
        
        # 3. Kiểm tra hành động hợp lệ (bảng có thay đổi không)
        if np.array_equal(old_board, new_board_np):
            # Nếu không di chuyển, trả về 0 reward và không thêm ô mới
            self.done = self._check_game_over()
            return self.board, 0, self.done 
        
        self.board = new_board_np
        self.score += score_gain
        
        # 4. Thêm ô mới và kiểm tra game over
        self.board = self._new_pieces(self.board)
        self.done = self._check_game_over()
        
        return self.board, reward, self.done