import pygame
import sys

from . import initboard, newpieces 

WIDTH, HEIGHT =1000, 700
pygame.init()
SCREEN_WIDTH = 400
score=0
SCREEN_SIZE = (SCREEN_WIDTH, 400)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("2048")
GRID_SIZE = 4
TILE_MARGIN = 10 
TILE_SIZE = (SCREEN_WIDTH - (GRID_SIZE + 1) * TILE_MARGIN) // GRID_SIZE
GRID_START_X = 300
GRID_START_Y = 200
FONT = pygame.font.Font(None, 40)

BACKGROUND_COLOR = (250, 248, 239) 
GRID_COLOR = (187, 173, 160)       
TILE_COLORS = { 0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121), # ... và các màu khác
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97), 
    512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46), }
TEXT_COLOR_DARK = (119, 110, 101)  
TEXT_COLOR_LIGHT = (249, 246, 242)


##Nút back
BACK_BTN_RECT = pygame.Rect(10, 10, 90, 40)

BACK_BTN_COLOR = (143, 122, 102)
BACK_BTN_HOVER = (156, 133, 116)
BUTTON_TEXT = (255, 255, 255)

BTN_FONT = pygame.font.SysFont("arial", 20, bold=True)

def draw_back_button():
    mouse_pos = pygame.mouse.get_pos()

    if BACK_BTN_RECT.collidepoint(mouse_pos):
        color = BACK_BTN_HOVER
    else:
        color = BACK_BTN_COLOR


    pygame.draw.rect(SCREEN, color, BACK_BTN_RECT, border_radius=8)


    text_surface = BTN_FONT.render("BACK", True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=BACK_BTN_RECT.center)
    SCREEN.blit(text_surface, text_rect)


def draw_over():
    global score
    score=0
    box_width = 300
    box_height = 100
    x = (WIDTH - box_width) // 2
    y = (HEIGHT - box_height) // 2
    pygame.draw.rect(SCREEN, 'black', [x, y, 300, 100], 0, 10)
    game_over_text1 = FONT.render('Game Over!', True, 'white')
    game_over_text2 = FONT.render('Play again?(y/n)', True, 'white')
    SCREEN.blit(game_over_text1, game_over_text1.get_rect(center=(x + box_width//2, y + 30)))
    SCREEN.blit(game_over_text2, game_over_text2.get_rect(center=(x + box_width//2, y + 70)))
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True    
                if event.key == pygame.K_n:
                    return False   

def draw_win():
    box_width = 300
    box_height = 100
    x = (WIDTH - box_width) // 2
    y = (HEIGHT - box_height) // 2
    pygame.draw.rect(SCREEN, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = FONT.render('You win', True, 'white')
    game_over_text2 = FONT.render('Continue?(y/n)', True, 'white')
    SCREEN.blit(game_over_text1, game_over_text1.get_rect(center=(x + box_width//2, y + 30)))
    SCREEN.blit(game_over_text2, game_over_text2.get_rect(center=(x + box_width//2, y + 70)))
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True    
                if event.key == pygame.K_n:
                    return False

def check_win(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 2048:
                return True
    return False
def check_game_over(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return False
            if c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
            if r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
    return True


def get_tile_position(row, col):
    x = GRID_START_X + col * (TILE_SIZE + TILE_MARGIN)
    y = GRID_START_Y + row * (TILE_SIZE + TILE_MARGIN)
    return x, y

def draw_tile(surface, row, col, value):
    x, y = get_tile_position(row, col)
    color = TILE_COLORS.get(value, TILE_COLORS[0])
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)
    if value > 0:
        text_surface = FONT.render(str(value), True, TEXT_COLOR_DARK if value < 8 else TEXT_COLOR_LIGHT)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        surface.blit(text_surface, text_rect)


def draw_grid(surface, board):
    grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
    grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
    pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(surface, row, col, board[row][col])


def drawboard(board, name):
    SCREEN.blit(BACKGROUND_IMG, (0, 0)) 
    
    draw_grid(SCREEN, board)
    
    draw_static_elements(SCREEN, name)
    
    draw_back_button()

def add_score(amount):
    global score
    score += amount

def compress(a):
    sub=[0,0,0,0]
    i=0
    for x in a:
        if (x!=0):
            sub[i]=x
            i+=1
    return sub
def merge(a):
    global score
    for i in range(3):
        if a[i]==a[i+1]:
            a[i]=a[i]*2
            add_score(a[i])
            a[i+1]=0
    return compress(a)
def combin(a):
    return merge(compress(a))

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
            new_board = newpieces(new_board)
            return new_board
            
    return current_board

def play(name):
    board=initboard()
    running=True
    global score
    score=0
    while running:
       
        drawboard(board,name)
        
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BTN_RECT.collidepoint(event.pos):
                    return 
            elif event.type == pygame.KEYDOWN:
                board = process_move_with_slide_animation(event,board,name)
                drawboard(board,name)
                pygame.display.update()
                if (check_game_over(board)):
                    restart=draw_over()
                    if restart:
                        board=initboard()
                    else:
                        running=False
                if (check_win(board)):
                    conti=draw_win()
                    if not conti:
                        board=initboard()

def animate_slide_tiles(surface, old_board, new_board, direction):
   
    frames = 10
    moving_tiles = []
    for row in range(4):
        for col in range(4):
            old_value = old_board[row][col]
            if old_value == 0:
                continue
            target_row, target_col = find_tile_destination(old_board, new_board, row, col, direction)
            
            if target_row != row or target_col != col:
                moving_tiles.append({
                    'value': old_value,
                    'from_row': row,
                    'from_col': col,
                    'to_row': target_row,
                    'to_col': target_col
                })
    for frame in range(frames + 1):
        progress = frame / frames
        surface.fill(BACKGROUND_COLOR)
        grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
        grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
        pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
        for row in range(4):
            for col in range(4):
                x = GRID_START_X + col * (TILE_SIZE + TILE_MARGIN)
                y = GRID_START_Y + row * (TILE_SIZE + TILE_MARGIN)
                pygame.draw.rect(surface, TILE_COLORS[0], (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)
        drawn_positions = set()
        for tile in moving_tiles:
            drawn_positions.add((tile['to_row'], tile['to_col']))   
        for row in range(4):
            for col in range(4):
                if (row, col) not in drawn_positions and new_board[row][col] != 0:
                    draw_tile_at_position(surface, row, col, new_board[row][col])
        for tile in moving_tiles:
            current_row = tile['from_row'] + (tile['to_row'] - tile['from_row']) * progress
            current_col = tile['from_col'] + (tile['to_col'] - tile['from_col']) * progress
            draw_tile_at_position(surface, current_row, current_col, tile['value'])
        
        pygame.display.update()
        pygame.time.delay(12)

def find_tile_destination(old_board, new_board, row, col, direction):

    value = old_board[row][col]
    if direction == 'left':
        for c in range(4):
            if new_board[row][c] != 0:
                if c <= col and (new_board[row][c] == value * 2 or new_board[row][c] == value):
                    return (row, c)
        return (row, 0)
    elif direction == 'right':
        for c in range(3, -1, -1):
            if new_board[row][c] != 0:
                if c >= col and (new_board[row][c] == value * 2 or new_board[row][c] == value):
                    return (row, c)
        return (row, 3)
    elif direction == 'up':
        for r in range(4):
            if new_board[r][col] != 0:
                if r <= row and (new_board[r][col] == value * 2 or new_board[r][col] == value):
                    return (r, col)
        return (0, col)
    elif direction == 'down':
        for r in range(3, -1, -1):
            if new_board[r][col] != 0:
                if r >= row and (new_board[r][col] == value * 2 or new_board[r][col] == value):
                    return (r, col)
        return (3, col)
    return (row, col)

def draw_tile_at_position(surface, row, col, value):
   
    x = GRID_START_X + col * (TILE_SIZE + TILE_MARGIN)
    y = GRID_START_Y + row * (TILE_SIZE + TILE_MARGIN)
    color = TILE_COLORS.get(value, TILE_COLORS[0])
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)
    if value > 0:
        text_color = TEXT_COLOR_DARK if value < 8 else TEXT_COLOR_LIGHT
        text_surface = FONT.render(str(value), True, text_color)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        surface.blit(text_surface, text_rect)

def animate_new_tile(surface, board, row, col, value):
   
   for step in range(5):
        scale = (step + 1) / 5
        x = GRID_START_X + col * (TILE_SIZE + TILE_MARGIN)
        y = GRID_START_Y + row * (TILE_SIZE + TILE_MARGIN)
        surface.fill(BACKGROUND_COLOR)
        grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
        grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
        pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
        for r in range(4):
            for c in range(4):
                x_empty = GRID_START_X + c * (TILE_SIZE + TILE_MARGIN)
                y_empty = GRID_START_Y + r * (TILE_SIZE + TILE_MARGIN)
                pygame.draw.rect(surface, TILE_COLORS[0], (x_empty, y_empty, TILE_SIZE, TILE_SIZE), border_radius=3)
        for r in range(4):
            for c in range(4):
                if board[r][c] != 0:
                    if r == row and c == col:
                        scaled_size = TILE_SIZE * scale
                        offset = (TILE_SIZE - scaled_size) / 2
                        scaled_x = x + offset
                        scaled_y = y + offset      
                        color = TILE_COLORS.get(value, TILE_COLORS[0])
                        pygame.draw.rect(surface, color, (scaled_x, scaled_y, scaled_size, scaled_size), border_radius=3)                   
                        if scale > 0.4:
                            text_color = TEXT_COLOR_DARK if value < 8 else TEXT_COLOR_LIGHT
                            font_size = int(40 * scale)
                            scaled_font = pygame.font.Font(None, font_size)
                            text_surface = scaled_font.render(str(value), True, text_color)
                            text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                            surface.blit(text_surface, text_rect)
                    else:                    
                        draw_tile_at_position(surface, r, c, board[r][c])
        pygame.display.update()
        pygame.time.delay(20)



def draw_full_game_state(surface, board, name=None, score_value=None):
   
    surface.blit(BACKGROUND_IMG, (0, 0))
    grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
    grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
    pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
    
    for r in range(4):
        for c in range(4):
            x = GRID_START_X + c * (TILE_SIZE + TILE_MARGIN)
            y = GRID_START_Y + r * (TILE_SIZE + TILE_MARGIN)
            pygame.draw.rect(surface, TILE_COLORS[0], (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)
    
    for r in range(4):
        for c in range(4):
            if board[r][c] != 0:
                draw_tile_at_position(surface, r, c, board[r][c])
    
    if score_value is not None:
        score_text = FONT.render(f'Score: {score_value}', True, TEXT_COLOR_DARK)
        surface.blit(score_text, (10, 410))
    
    if name is not None:
        name_surface = FONT.render(name, True, TEXT_COLOR_DARK)
        name_rect = name_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        surface.blit(name_surface, name_rect)


def draw_static_elements(surface, name=None):
    global score
    
    font_label = pygame.font.Font(None, 28)
    font_value = pygame.font.Font(None, 36)
    top_y = GRID_START_Y - 80 


    if name:
        name_txt = font_value.render(f"PLAYER: {name}", True, TEXT_COLOR_DARK)
        surface.blit(name_txt, (GRID_START_X, top_y + 25))

    score_val = font_value.render(f"SCORE: {score}", True, TEXT_COLOR_DARK)
    score_val_rect = score_val.get_rect(topright=(GRID_START_X + 400 - TILE_MARGIN, top_y + 25))
    surface.blit(score_val, score_val_rect)
    

    draw_back_button()


def draw_board_only(surface, board):
    grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
    grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
    pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
    

    for r in range(4):
        for c in range(4):
            x = GRID_START_X + c * (TILE_SIZE + TILE_MARGIN)
            y = GRID_START_Y + r * (TILE_SIZE + TILE_MARGIN)
            pygame.draw.rect(surface, TILE_COLORS[0], (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)
    

    for r in range(4):
        for c in range(4):
            if board[r][c] != 0:
                draw_tile_at_position(surface, r, c, board[r][c])


def animate_slide_tiles_fixed(surface, old_board, new_board, direction, name=None):
    clock = pygame.time.Clock()
    frames = 12 
    moving_tiles = []
    

    for row in range(4):
        for col in range(4):
            old_value = old_board[row][col]
            if old_value == 0: continue
            target_row, target_col = find_tile_destination(old_board, new_board, row, col, direction)
            if target_row != row or target_col != col:
                moving_tiles.append({
                    'value': old_value,
                    'from_row': row, 'from_col': col,
                    'to_row': target_row, 'to_col': target_col
                })
    
    for frame in range(frames + 1):
        progress = frame / frames
        surface.blit(BACKGROUND_IMG, (0, 0))
        draw_static_elements(surface, name)
        
        grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
        grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
        pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)
        for r in range(4):
            for c in range(4):
                px, py = get_tile_position(r, c)
                pygame.draw.rect(surface, TILE_COLORS[0], (px, py, TILE_SIZE, TILE_SIZE), border_radius=3)

        moved_destinations = {(t['to_row'], t['to_col']) for t in moving_tiles}
        for r in range(4):
            for c in range(4):
                if (r, c) not in moved_destinations and new_board[r][c] != 0:
                    draw_tile_at_position(surface, r, c, new_board[r][c])

        for tile in moving_tiles:
            curr_row = tile['from_row'] + (tile['to_row'] - tile['from_row']) * progress
            curr_col = tile['from_col'] + (tile['to_col'] - tile['from_col']) * progress
            draw_tile_at_position(surface, curr_row, curr_col, tile['value'])

        pygame.display.update()
        clock.tick(120) 

def animate_new_tile_fixed(surface, board, row, col, value, name=None):
    clock = pygame.time.Clock()
    steps = 8 
    
    for step in range(steps + 1):
        scale = step / steps
        surface.blit(BACKGROUND_IMG, (0, 0))
        draw_static_elements(surface, name)
        
        draw_board_only(surface, board)
        
        x, y = get_tile_position(row, col)
        scaled_size = TILE_SIZE * scale
        offset = (TILE_SIZE - scaled_size) / 2
        
        color = TILE_COLORS.get(value, TILE_COLORS[0])
        pygame.draw.rect(surface, color, (x + offset, y + offset, scaled_size, scaled_size), border_radius=3)
        
        pygame.display.update()
        clock.tick(120)
def process_move_with_slide_animation(event, current_board, name=None):
    key_map = {
        pygame.K_LEFT: ('a', 'left'),
        pygame.K_RIGHT: ('d', 'right'),
        pygame.K_UP: ('w', 'up'),
        pygame.K_DOWN: ('s', 'down'),
    }
    
    if event.key in key_map:
        key_char, direction = key_map[event.key]
        old_board = [row[:] for row in current_board]
        new_board = update_board(current_board, key_char)
        
        if new_board != old_board:
            animate_slide_tiles_fixed(SCREEN, old_board, new_board, direction, name) 
            
            drawboard(new_board, name) 
            
            board_before_new = [row[:] for row in new_board]
            new_board = newpieces(new_board)
            for row in range(4):
                for col in range(4):
                    if board_before_new[row][col] == 0 and new_board[row][col] != 0:
                        animate_new_tile_fixed(SCREEN, new_board, row, col, new_board[row][col], name)
                        break
            
            return new_board
    
    return current_board
BACKGROUND_IMG = pygame.image.load('2048.png').convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))
