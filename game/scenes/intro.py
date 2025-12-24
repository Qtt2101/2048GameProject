import pygame
import sys
import math
from . import board

BACKGROUND_COLOR = (250, 248, 239)
def run_intro_v2():
    pygame.init()
    WIDTH, HEIGHT = 1000, 700
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 - NHÓM 5")
    
    clock = pygame.time.Clock()
    animation_offset = 0
    star_positions = generate_random_stars(15)
    cloud_positions = generate_clouds(5)
    
    big_cloud = {'x': 500, 'y': 420, 'size': 1.8, 'speed': 15}
    
    buttons = create_menu_buttons_v2_fixed()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        animation_offset += dt
        
        draw_background_v2(SCREEN, WIDTH, HEIGHT, animation_offset, cloud_positions)
        
        
        draw_sun_v2(SCREEN, animation_offset)
        
        draw_decorative_stars_v2(SCREEN, star_positions, animation_offset)
        draw_fireworks_v2(SCREEN, WIDTH, HEIGHT, animation_offset)
        draw_title_v2_fixed(SCREEN, WIDTH)
        
        draw_big_cloud_center_v2(SCREEN, big_cloud, animation_offset, WIDTH)
        
        draw_mascot_area_v2(SCREEN, WIDTH, HEIGHT, animation_offset)
        
        draw_airplanes_bottom_v2(SCREEN, WIDTH, HEIGHT, animation_offset)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw_v2(SCREEN, mouse_pos, animation_offset)
        
        draw_footer_credit_v2_fixed(SCREEN, WIDTH, HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        result = button.callback(SCREEN, WIDTH, HEIGHT)
                        if result == "quit":
                            running = False
        
        pygame.display.flip()

def get_vietnamese_font(size, bold=False):
    
    font_names = [
        'Arial Unicode MS',  
        'Segoe UI',
        'Arial',
        'Tahoma',
        'Verdana',
        'Times New Roman',
        'DejaVu Sans',
        'FreeSans',
        'Liberation Sans',
        'Noto Sans'
    ]
    
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            if font:
                return font
        except:
            continue
    return pygame.font.Font(None, size)
def draw_sun_v2(screen, time_offset):
    
    sun_x = 80
    sun_y = 80
    
    num_rays = 12
    for i in range(num_rays):
        angle = (2 * math.pi * i / num_rays) + (time_offset * 0.5)
       
        start_distance = 35
        end_distance = 55
        start_x = sun_x + start_distance * math.cos(angle)
        start_y = sun_y + start_distance * math.sin(angle)
        end_x = sun_x + end_distance * math.cos(angle)
        end_y = sun_y + end_distance * math.sin(angle)
        
        pygame.draw.line(screen, (255, 200, 0), (start_x, start_y), (end_x, end_y), 4)
    
    pygame.draw.circle(screen, (255, 100, 80), (sun_x, sun_y), 32, 4)
   
    pygame.draw.circle(screen, (255, 220, 50), (sun_x, sun_y), 28)
    
    eye_y = sun_y - 8
    pygame.draw.circle(screen, (50, 50, 50), (sun_x - 8, eye_y), 3)
    pygame.draw.circle(screen, (50, 50, 50), (sun_x + 8, eye_y), 3)
    
    smile_rect = pygame.Rect(sun_x - 12, sun_y + 2, 24, 12)
    pygame.draw.arc(screen, (50, 50, 50), smile_rect, math.pi, 2 * math.pi, 2)

def draw_big_cloud_center_v2(screen, cloud, time_offset, width):
   
    cloud['x'] += cloud['speed'] * 0.016
    
    
    if cloud['x'] > width + 150:
        cloud['x'] = -150
    
    draw_cloud_v2(screen, cloud['x'], cloud['y'], cloud['size'])

def draw_airplanes_bottom_v2(screen, width, height, time_offset):
    
    planes = [
        {'base_x': 50, 'y': height - 100, 'phase': 0},
        {'base_x': 120, 'y': height - 140, 'phase': 1.5},
        {'base_x': 190, 'y': height - 110, 'phase': 3}
    ]
    
    for plane in planes:
      
        bounce = math.sin(time_offset * 1.5 + plane['phase']) * 8
        x = plane['base_x']
        y = plane['y'] + bounce
        
        draw_single_airplane_v2(screen, x, y, (100, 170, 230))

def draw_single_airplane_v2(screen, x, y, color):
  
    body_points = [
        (x - 15, y),
        (x + 20, y - 3),
        (x + 25, y),
        (x + 20, y + 3)
    ]
    pygame.draw.polygon(screen, color, body_points)
    
    wing_top = [
        (x - 5, y - 3),
        (x + 5, y - 12),
        (x + 10, y - 3)
    ]
    pygame.draw.polygon(screen, color, wing_top)
    
   
    wing_bottom = [
        (x - 5, y + 3),
        (x + 5, y + 12),
        (x + 10, y + 3)
    ]
    pygame.draw.polygon(screen, color, wing_bottom)
    
    tail = [
        (x - 15, y),
        (x - 20, y - 8),
        (x - 12, y)
    ]
    pygame.draw.polygon(screen, color, tail)
    
    pygame.draw.circle(screen, (255, 255, 255), (int(x + 5), int(y)), 3)

def generate_random_stars(count):
   
    import random
    stars = []
    for i in range(count):
        x = random.randint(50, 950)
        y = random.randint(50, 650)
        size = random.randint(15, 35)
        color_choice = random.choice(['yellow', 'orange', 'blue', 'green'])
        stars.append({'x': x, 'y': y, 'size': size, 'color': color_choice, 'phase': random.random() * math.pi * 2})
    return stars

def generate_clouds(count):
    
    import random
    clouds = []
    for i in range(count):
        x = random.randint(-100, 1000)
        y = random.randint(50, 200)
        size = random.uniform(0.5, 1.2)
        speed = random.uniform(10, 30)
        clouds.append({'x': x, 'y': y, 'size': size, 'speed': speed})
    return clouds

def draw_background_v2(screen, width, height, time_offset, clouds):
   
    screen.fill((245, 240, 230))
    
    draw_decorative_blob(screen, 100, 80, 180, (255, 160, 130), 0.7)
    draw_decorative_blob(screen, width - 150, 100, 200, (150, 200, 250), 0.6)
    
    for cloud in clouds:
        cloud['x'] += cloud['speed'] * 0.016
        if cloud['x'] > width + 100:
            cloud['x'] = -100
        draw_cloud_v2(screen, cloud['x'], cloud['y'], cloud['size'])
    
    draw_bushes_v2(screen, width, height)

def draw_decorative_blob(screen, x, y, radius, color, alpha):
   
    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (*color, int(255 * alpha)), (radius, radius), radius)
    screen.blit(s, (x - radius, y - radius))

def draw_cloud_v2(screen, x, y, size):
    
    cloud_color = (255, 255, 255, 180)
    s = pygame.Surface((int(120 * size), int(60 * size)), pygame.SRCALPHA)
    
    pygame.draw.ellipse(s, cloud_color, (0, 20, 40 * size, 35 * size))
    pygame.draw.ellipse(s, cloud_color, (25 * size, 10, 50 * size, 40 * size))
    pygame.draw.ellipse(s, cloud_color, (50 * size, 15, 45 * size, 38 * size))
    
    screen.blit(s, (int(x), int(y)))

def draw_bushes_v2(screen, width, height):
    
    green_shades = [(100, 180, 130), (120, 200, 150), (90, 170, 120)]
    
    for i, color in enumerate(green_shades):
        pygame.draw.circle(screen, color, (80 + i * 30, height - 60 + i * 10), 50 - i * 5)
    
    for i, color in enumerate(green_shades[::-1]):
        pygame.draw.circle(screen, color, (width - 100 + i * 25, height - 70 + i * 8), 45 - i * 5)

def draw_decorative_stars_v2(screen, stars, time_offset):
    
    color_map = {
        'yellow': (255, 220, 100),
        'orange': (255, 160, 100),
        'blue': (150, 200, 255),
        'green': (150, 220, 150)
    }
    
    for star in stars:
        scale = 0.8 + 0.2 * math.sin(time_offset * 2 + star['phase'])
        color = color_map[star['color']]
        draw_star_shape(screen, star['x'], star['y'], star['size'] * scale, color)

def draw_star_shape(screen, x, y, size, color):
   
    points = []
    for i in range(10):
        angle = math.pi / 2 + (2 * math.pi * i / 10)
        radius = size if i % 2 == 0 else size * 0.4
        px = x + radius * math.cos(angle)
        py = y - radius * math.sin(angle)
        points.append((px, py))
    
    if len(points) >= 3:
        pygame.draw.polygon(screen, color, points)

def draw_fireworks_v2(screen, width, height, time_offset):
    
    draw_simple_firework(screen, 450, 180, time_offset, (255, 180, 100))
    draw_simple_firework(screen, 750, 200, time_offset + 1.5, (255, 200, 150))

def draw_simple_firework(screen, x, y, time_offset, color):
   
    for i in range(8):
        angle = (2 * math.pi * i / 8) + time_offset
        distance = 20 + 10 * math.sin(time_offset * 3)
        end_x = x + distance * math.cos(angle)
        end_y = y + distance * math.sin(angle)
        pygame.draw.line(screen, color, (x, y), (end_x, end_y), 3)

def draw_title_v2_fixed(screen, width):
    
    title_font = get_vietnamese_font(90)
    subtitle_font = get_vietnamese_font(65)
    
    
    title1 = title_font.render("GROUP", True, (255, 140, 100))
    title1_outline = title_font.render("GROUP", True, (100, 60, 40))
    
    
    title2 = subtitle_font.render("FIVE", True, (120, 180, 230))
    title2_outline = subtitle_font.render("FIVE", True, (50, 80, 120))
    
    
    screen.blit(title1_outline, (155 + 3, 82 + 3))
    screen.blit(title1, (155, 82))
    
    screen.blit(title2_outline, (180 + 3, 155 + 3))
    screen.blit(title2, (180, 155))

def draw_mascot_area_v2(screen, width, height, time_offset):
    
    start_x = width - 380
    base_y = height // 2 + 20
    
    digits = ['2', '0', '4', '8']
    colors = [
        (255, 140, 100),
        (120, 180, 230),
        (120, 200, 150),
        (255, 200, 100)
    ]
    
    for i, (digit, color) in enumerate(zip(digits, colors)):
        phase = time_offset * 2.5 + (i * 0.5)
        bounce = math.sin(phase) * 15
        scale = 1.0 + math.sin(phase) * 0.1
        
        x_pos = start_x + i * 85
        y_pos = base_y + bounce
        
        draw_3d_digit(screen, digit, x_pos, y_pos, color, scale)
    
    draw_sparkles_around_2048(screen, start_x, base_y, time_offset)

def draw_3d_digit(screen, digit, x, y, color, scale=1.0):
   
    digit_font = get_vietnamese_font(int(90 * scale))
    
    shadow_color = tuple(max(0, c - 80) for c in color)
    border_color = tuple(max(0, c - 40) for c in color)
   
    shadow_surface = digit_font.render(digit, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(int(x + 4), int(y + 4)))
    screen.blit(shadow_surface, shadow_rect)
    
    border_surface = digit_font.render(digit, True, border_color)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        border_rect = border_surface.get_rect(center=(int(x + dx), int(y + dy)))
        screen.blit(border_surface, border_rect)
    
   
    digit_surface = digit_font.render(digit, True, color)
    digit_rect = digit_surface.get_rect(center=(int(x), int(y)))
    screen.blit(digit_surface, digit_rect)
    
    highlight_color = tuple(min(255, c + 60) for c in color)
    highlight_font = get_vietnamese_font(int(85 * scale))
    highlight_surface = highlight_font.render(digit, True, highlight_color)
    highlight_rect = highlight_surface.get_rect(center=(int(x - 1), int(y - 2)))
    
    highlight_with_alpha = pygame.Surface(highlight_surface.get_size(), pygame.SRCALPHA)
    highlight_with_alpha.fill((0, 0, 0, 0))
    highlight_with_alpha.blit(highlight_surface, (0, 0))
    highlight_with_alpha.set_alpha(120)
    screen.blit(highlight_with_alpha, highlight_rect)

def draw_sparkles_around_2048(screen, center_x, center_y, time_offset):
    
    sparkle_positions = [
        (center_x + 150, center_y - 80),
        (center_x + 300, center_y - 60),
        (center_x + 100, center_y + 70),
        (center_x + 280, center_y + 80),
        (center_x + 50, center_y - 40),
        (center_x + 350, center_y + 20)
    ]
    
    sparkle_colors = [
        (255, 220, 100),
        (255, 180, 150),
        (200, 200, 255),
        (150, 255, 200)
    ]
    
    for i, (x, y) in enumerate(sparkle_positions):
        phase = time_offset * 3 + i * 0.7
        alpha = abs(math.sin(phase))
        
        if alpha > 0.3:
            color = sparkle_colors[i % len(sparkle_colors)]
            size = 4 + int(alpha * 6)
            draw_sparkle_star(screen, x, y, size, color, alpha)

def draw_sparkle_star(screen, x, y, size, color, alpha):
   
    pygame.draw.line(screen, color, (x - size, y), (x + size, y), 2)
    pygame.draw.line(screen, color, (x, y - size), (x, y + size), 2)
    pygame.draw.line(screen, color, 
                    (x - size * 0.7, y - size * 0.7), 
                    (x + size * 0.7, y + size * 0.7), 2)
    pygame.draw.line(screen, color, 
                    (x - size * 0.7, y + size * 0.7), 
                    (x + size * 0.7, y - size * 0.7), 2)
    pygame.draw.circle(screen, color, (int(x), int(y)), max(2, int(size * 0.3)))

def draw_footer_credit_v2_fixed(screen, width, height):
    
    credit_font = get_vietnamese_font(26)
    credit_text = credit_font.render("PROJECT PYTHON - GROUP 5", True, (119, 110, 101))
    credit_rect = credit_text.get_rect(center=(width // 2, height - 30))
    screen.blit(credit_text, credit_rect)

class MenuButtonV2:
    def __init__(self, text, x, y, width, height, callback, color_theme='blue'):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color_theme = color_theme
        self.hover_scale = 1.0
        self.target_scale = 1.0
        
        self.colors = {
            'blue': {'main': (120, 180, 230), 'hover': (150, 200, 250), 'border': (80, 140, 200)},
            'orange': {'main': (255, 160, 130), 'hover': (255, 180, 150), 'border': (220, 120, 90)},
            'green': {'main': (120, 200, 150), 'hover': (150, 220, 180), 'border': (90, 160, 120)},
            'purple': {'main': (180, 150, 220), 'hover': (200, 170, 240), 'border': (140, 110, 180)},
            'red': {'main': (200, 50, 50), 'hover': (230, 80, 80), 'border': (150, 30, 30)} 
        }
    
    def draw_v2(self, screen, mouse_pos, time_offset):
       
        is_hover = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.08 if is_hover else 1.0
        
        self.hover_scale += (self.target_scale - self.hover_scale) * 0.15
        
        colors = self.colors.get(self.color_theme, self.colors['blue'])
        current_color = colors['hover'] if is_hover else colors['main']
        
        scaled_width = int(self.rect.width * self.hover_scale)
        scaled_height = int(self.rect.height * self.hover_scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        shadow_rect = scaled_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=25)
        
        pygame.draw.rect(screen, colors['border'], scaled_rect, border_radius=25)
        
        inner_rect = scaled_rect.inflate(-6, -6)
        pygame.draw.rect(screen, current_color, inner_rect, border_radius=22)
        
        font = get_vietnamese_font(42)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def create_menu_buttons_v2_fixed():
    button_width = 250
    button_height = 65
    start_x = 150
    start_y = 300
    spacing = 85
    
    buttons = [
        MenuButtonV2("Play", start_x, start_y, button_width, button_height, 
                    handle_new_game_v2, 'orange'),
        MenuButtonV2("AI Mode", start_x, start_y + spacing, button_width, button_height, 
                    handle_ai_mode_v2_fixed, 'green'),
        MenuButtonV2("Credit", start_x, start_y + spacing * 2, button_width, button_height, 
                    handle_credit_v2_fixed, 'purple'),
        MenuButtonV2("Exit", start_x, start_y + spacing * 3, button_width, button_height,  
                    handle_exit_game_v2, 'red'),  
    ]
    
    return buttons

def handle_new_game_v2(screen, width, height):
    player_name = show_name_input_dialog_v2(screen, width, height)
    if player_name and player_name.strip():
        board.play(player_name)
    return None

def handle_ai_mode_v2_fixed(screen, width, height):
    show_message_dialog_v2_fixed(screen, width, height, "AI Mode", 
                          "AI MODE\n NOT DEVELOPMENT!", 
                          (120, 200, 150))
    return None

def handle_credit_v2_fixed(screen, width, height):
    show_credit_dialog_v2_fixed(screen, width, height)
    return None
def handle_exit_game_v2(screen, width, height):
    return "quit"

def show_name_input_dialog_v2(screen, width, height):
    dialog_width = 500
    dialog_height = 300
    dialog_x = (width - dialog_width) // 2
    dialog_y = (height - dialog_height) // 2
    
    input_box = pygame.Rect(dialog_x + 50, dialog_y + 140, dialog_width - 100, 60)
    player_name = ""
    
    
    title_font = get_vietnamese_font(48)
    input_font = get_vietnamese_font(42)
    hint_font = get_vietnamese_font(28)
    
    active = True
    clock = pygame.time.Clock()
    
    while active:
        clock.tick(60)
        screen.fill(BACKGROUND_COLOR)
        
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect, border_radius=20)
        pygame.draw.rect(screen, (120, 180, 230), dialog_rect, 4, border_radius=20)
        
        title_surface = title_font.render("ENTER YOUR NAME", True, (255, 140, 100))
        title_rect = title_surface.get_rect(center=(width // 2, dialog_y + 60))
        screen.blit(title_surface, title_rect)
        
        pygame.draw.rect(screen, (240, 240, 240), input_box, border_radius=10)
        pygame.draw.rect(screen, (120, 180, 230), input_box, 3, border_radius=10)
        
        text_surface = input_font.render(player_name, True, (50, 50, 50))
        screen.blit(text_surface, (input_box.x + 15, input_box.y + 15))
        
        hint_text = hint_font.render("ENTER TO CONTINUE AND ESC TO QUIT", True, (119, 110, 101))
        hint_rect = hint_text.get_rect(center=(width // 2, dialog_y + dialog_height - 40))
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip():
                        return player_name
                elif event.key == pygame.K_ESCAPE:  
                    return None  
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 15:
                        player_name += event.unicode
    
    return None
def show_message_dialog_v2_fixed(screen, width, height, title, message, title_color):
    dialog_width = 500
    dialog_height = 280
    dialog_x = (width - dialog_width) // 2
    dialog_y = (height - dialog_height) // 2
    
    title_font = get_vietnamese_font(48, bold=True)
    message_font = get_vietnamese_font(36, bold=False)
    hint_font = get_vietnamese_font(26, bold=False)
    
    active = True
    clock = pygame.time.Clock()
    
    while active:
        clock.tick(60)
        
        screen.fill(BACKGROUND_COLOR)
        
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        screen.fill(BACKGROUND_COLOR)
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect, border_radius=20)
        pygame.draw.rect(screen, title_color, dialog_rect, 4, border_radius=20)
        
        title_surface = title_font.render(title, True, title_color)
        title_rect = title_surface.get_rect(center=(width // 2, dialog_y + 50))
        screen.blit(title_surface, title_rect)
        
        lines = message.split('\n')
        for i, line in enumerate(lines):
            msg_surface = message_font.render(line, True, (80, 80, 80))
            msg_rect = msg_surface.get_rect(center=(width // 2, dialog_y + 130 + i * 45))
            screen.blit(msg_surface, msg_rect)
        
        hint_text = hint_font.render("Press any key to close", True, (119, 110, 101))
        hint_rect = hint_text.get_rect(center=(width // 2, dialog_y + dialog_height - 35))
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                active = False
    
    return None

def show_credit_dialog_v2_fixed(screen, width, height):
    dialog_width = 600
    dialog_height = 500
    dialog_x = (width - dialog_width) // 2
    dialog_y = (height - dialog_height) // 2
    
    title_font = get_vietnamese_font(56, bold=True)
    name_font = get_vietnamese_font(38, bold=True)
    info_font = get_vietnamese_font(30, bold=True)
    member_font = get_vietnamese_font(24, bold=False)
    
    active = True
    clock = pygame.time.Clock()
    
    while active:
        clock.tick(60)
        
        screen.fill(BACKGROUND_COLOR)
        
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect, border_radius=20)
        pygame.draw.rect(screen, (180, 150, 220), dialog_rect, 4, border_radius=20)
        
        title_surface = title_font.render("PROFILE GROUP", True, (180, 150, 220))
        title_rect = title_surface.get_rect(center=(width // 2, dialog_y + 50))
        screen.blit(title_surface, title_rect)
        
        y_offset = dialog_y + 110
        
        project_text = name_font.render("PROJECT PYTH0N - GAME 2048", True, (255, 140, 100))
        project_rect = project_text.get_rect(center=(width // 2, y_offset))
        screen.blit(project_text, project_rect)
        
        y_offset += 50
        
        team_text = info_font.render("GROUP 5", True, (80, 80, 80))
        team_rect = team_text.get_rect(center=(width // 2, y_offset))
        screen.blit(team_text, team_rect)
        
        y_offset += 45
        
        members = [
            "Nguyen Van Phi Long - 25120206",
            "Quan Tien Thinh - 25120234",
            "Vuong Dang Khoa - 25120198",
            "Van Dang Khoa - 25120197",
            "Duong Hai My - 25120211",
            "Tran Nguyen Bao Tam - 25120229",
        ]
        
        for member in members:
            member_text = member_font.render(member, True, (100, 100, 100))
            member_rect = member_text.get_rect(center=(width // 2, y_offset))
            screen.blit(member_text, member_rect)
            y_offset += 32
        
        hint_font = get_vietnamese_font(26, bold=False)
        hint_text = hint_font.render("Press any key to close.", True, (119, 110, 101))
        hint_rect = hint_text.get_rect(center=(width // 2, dialog_y + dialog_height - 35))
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                active = False