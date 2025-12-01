import pygame
import sys

import __init__ as logic 


pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Trò Chơi 2048")

GRID_SIZE = 4
TILE_MARGIN = 10 
TILE_SIZE = (SCREEN_WIDTH - (GRID_SIZE + 1) * TILE_MARGIN) // GRID_SIZE
GRID_START_X = TILE_MARGIN 
GRID_START_Y = TILE_MARGIN 
FONT = pygame.font.Font(None, 40)

BACKGROUND_COLOR = (250, 248, 239) 
GRID_COLOR = (187, 173, 160)       
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR_DARK = (119, 110, 101)  
TEXT_COLOR_LIGHT = (249, 246, 242) 



def get_tile_position(row, col):
    """Tính toán tọa độ x, y cho ô (row, col)"""
    x = GRID_START_X + col * (TILE_SIZE + TILE_MARGIN)
    y = GRID_START_Y + row * (TILE_SIZE + TILE_MARGIN)
    return x, y

def draw_tile(surface, row, col, value):
    """Vẽ một ô với giá trị số của nó."""
    x, y = get_tile_position(row, col)
    
    
    color = TILE_COLORS.get(value, TILE_COLORS[0])
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=3)

    
    if value > 0:
        text_surface = FONT.render(str(value), True, TEXT_COLOR_DARK if value < 8 else TEXT_COLOR_LIGHT)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        surface.blit(text_surface, text_rect)


def draw_grid(surface, board):
    """Vẽ toàn bộ khung lưới và các ô số dựa trên trạng thái bảng."""
    
    grid_width = SCREEN_WIDTH - 2 * TILE_MARGIN
    grid_rect = pygame.Rect(GRID_START_X, GRID_START_Y, grid_width, grid_width)
    pygame.draw.rect(surface, GRID_COLOR, grid_rect, border_radius=6)

   
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(surface, row, col, board[row][col])


def main():
    
  
    logic.board_values, _ = logic.newpieces(logic.board_values) 
    logic.board_values, _ = logic.newpieces(logic.board_values) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # TODO
            if event.type == pygame.KEYDOWN:
                pass 

       
        SCREEN.fill(BACKGROUND_COLOR)

        
        draw_grid(SCREEN, logic.board_values) 

       
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()