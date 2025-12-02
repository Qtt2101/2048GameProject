import random
board_values = [[0 for _ in range(4)] for _ in range(4)]
def newpieces(board):
    empt=[]
    for i in range(4):
        for j in range(4):
             if board[i][j]==0:
                 empt.append((i,j))
    if len(empt)==0:
        return board,True
    x,y=random.choice(empt)
    if random.randint(1,10)==1:
        board[x][y]=4
    else:
        board[x][y]=2
    return board,False
