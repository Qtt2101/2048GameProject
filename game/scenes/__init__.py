import random
def newpieces(board):
    empt=[]
    for i in range(4):
        for j in range(4):
             if board[i][j]==0:
                 empt.append((i,j))
    x,y=random.choice(empt)
    if random.randint(1,10)==1:
        board[x][y]=4
    else:
        board[x][y]=2
    return board
def initboard():
    board_values = [[0 for _ in range(4)] for _ in range(4)]
    board_values=newpieces(board_values)
    board_values=newpieces(board_values)
    return board_values
    
