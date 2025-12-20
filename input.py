import __init__
def reverse(board):
    new_board = []
    for row in board:
        new_board.append(row[::-1])
    return new_board

def transpose(board):
    return [list(row) for row in zip(*board)]

def update_board(board, key):
    new_board = []
    
    if key == 'a':
        for row in board:
            new_board.append(combin(row))
            
    elif key == 'd':
        temp_board = reverse(board)
        processed_board = []
        for row in temp_board:
            processed_board.append(combin(row))
        new_board = reverse(processed_board)
        
    elif key == 'w':
        temp_board = transpose(board)
        processed_board = []
        for row in temp_board:
            processed_board.append(combin(row))
        new_board = transpose(processed_board)
        
    elif key == 's':
        temp_board = transpose(board)
        temp_board = reverse(temp_board)
        processed_board = []
        for row in temp_board:
            processed_board.append(combin(row))
        new_board = reverse(processed_board)
        new_board = transpose(new_board)
        
    else:
        return board

    return new_board

import pygame
def process_move(event, current_board):
    key_map = {
        pygame.K_LEFT: 'a',
        pygame.K_RIGHT: 'd',
        pygame.K_UP: 'w',
        pygame.K_DOWN: 's',
    }
        
    if event.key in key_map:
        key_char = key_map[event.key]
            
        old_board = [row[:] for row in current_board]
            
        new_board = update_board(current_board, key_char) 
            
        if new_board != old_board:
            new_board = __init__.newpieces(new_board)
            return new_board
            
    return current_board
