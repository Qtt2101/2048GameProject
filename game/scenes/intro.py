import pygame
import sys


def run_intro():

    pygame.init()
    WIDTH, HEIGHT = 400, 500
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("2048 Menu")

    BG_COLOR = (250, 248, 239)
    TEXT_COLOR = (119, 110, 101)
    BUTTON_COLOR = (143, 122, 102)
    BUTTON_HOVER = (156, 133, 116)
    WHITE = (255, 255, 255)

    TITLE_FONT = pygame.font.Font(None, 100)
    BUTTON_FONT = pygame.font.Font(None, 36)
    CREDIT_FONT = pygame.font.Font(None, 24)
    INPUT_FONT = pygame.font.Font(None, 40)

    player_name = ""
    input_box = pygame.Rect(120, 430, 160, 50)

    class Button:
        def __init__(self, text, x, y, width, height, callback):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.callback = callback
            self.color = BUTTON_COLOR

        def draw(self, screen):
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else self.color
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            text_surf = BUTTON_FONT.render(self.text, True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def check_click(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()
    def start_new_game():
        nonlocal player_name
        player_name = ""

        entering = True
        while entering:
            SCREEN.fill(BG_COLOR)
            width, height = SCREEN.get_size()

            prompt_surface = INPUT_FONT.render("Enter Name:", True, TEXT_COLOR)
            SCREEN.blit(prompt_surface, (width // 2 - prompt_surface.get_width() // 2, 200))

            input_box.center = (width // 2, 260)
            pygame.draw.rect(SCREEN, WHITE, input_box, 0, border_radius=8)
            pygame.draw.rect(SCREEN, TEXT_COLOR, input_box, 2, border_radius=8)

            text_surface = INPUT_FONT.render(player_name, True, TEXT_COLOR)
            SCREEN.blit(text_surface, (input_box.x + 10, input_box.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip() != "":
                            print(f"Xin chào, {player_name}! Bắt đầu trò chơi...")
                            entering = False
                              
                        else:
                            print("Tên không được để trống!")
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15:
                            player_name += event.unicode
    def play_with_ai():
        pass

    def exit_game():
        pygame.quit()
        sys.exit()

    buttons = [
        Button("New Game", 120, 220, 160, 50, start_new_game),
        Button("Play with AI", 120, 290, 160, 50, play_with_ai),
        Button("Exit", 120, 360, 160, 50, exit_game)
    ]

    running = True
    clock = pygame.time.Clock()

    while running:
        SCREEN.fill(BG_COLOR)
        width, height = SCREEN.get_size()

        title_surface = TITLE_FONT.render("2048", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(width // 2, 120))
        SCREEN.blit(title_surface, title_rect)

        for i, button in enumerate(buttons):
            button.rect.centerx = width // 2
            button.rect.y = 220 + i * 70
            button.draw(SCREEN)

        credit_surface = CREDIT_FONT.render("D0 AN PYTH0N - NH0M 5", True, TEXT_COLOR)
        credit_rect = credit_surface.get_rect(center=(width // 2, height - 30))
        SCREEN.blit(credit_surface, credit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            for button in buttons:
                button.check_click(event)

        pygame.display.flip()
        clock.tick(60)






       
