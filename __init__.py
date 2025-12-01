import random

# Biến bảng trò chơi 4x4
board_values = [[0 for _ in range(4)] for _ in range(4)]

def newpieces(board):
    """
    Thêm một ô số 2 hoặc 4 ngẫu nhiên vào bảng.
    Trả về: (board, full_status)
    """
    empt = []
    for i in range(4):
        for j in range(4):
             if board[i][j] == 0:
                 empt.append((i, j))
    
    if len(empt) == 0:
        return board, True  # Bảng đã đầy
        
    x, y = random.choice(empt)
    # 90% là 2, 10% là 4
    if random.randint(1, 10) == 1:
        board[x][y] = 4
    else:
        board[x][y] = 2
        
    return board, False

# Hạn chế: Logic di chuyển chưa có ở đây.
