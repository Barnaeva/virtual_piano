import pygame
from utils.config import *
from utils.buttons import ImageButton
from utils.auth_system import AuthSystem


class LicenseScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.auth_system = AuthSystem()
        self.license_file = "piano_subscription.txt"
        # Введенный код
        self.input_code = ""

        # Кнопки
        self.submit_button = ImageButton(
            WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "ПРОВЕРИТЬ",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH,)

        self.exit_button = ImageButton(
            WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, "ВЫЙТИ",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH
        )

        self.font = pygame.font.SysFont(FONT, 36)
        self.small_font = pygame.font.SysFont(FONT, 24)

        self.verified = False
        self.message = ""
        self.show_demo_info = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_code()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_code = self.input_code[:-1]
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                                   pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                   pygame.K_8, pygame.K_9]:
                    # Преобразуем код клавиши в цифру
                    key_map = {
                        pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2',
                        pygame.K_3: '3', pygame.K_4: '4', pygame.K_5: '5',
                        pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8',
                        pygame.K_9: '9'
                    }
                    self.input_code += key_map[event.key]
                elif event.unicode.isdigit():  # Только цифры
                    if len(self.input_code) < 4:
                        self.input_code += event.unicode

            if self.submit_button.handle_event(event):
                self.check_code()

            if self.exit_button.handle_event(event):
                return False

        return True


    def check_code(self):

        if not self.input_code:
            self.message = "Введите код"
            return

        # Проверяем код
        if self.auth_system.check_code(self.input_code):
            try:
                from datetime import datetime
                today = datetime.now().strftime('%Y-%m-%d')

                with open(self.license_file, 'w') as f:
                    f.write(today)

                self.verified = True
                self.message = "Доступ открыт на 30 дней!"

            except Exception as e:
                print(f"Error: {e}")
        else:
            self.message = "Неверный код доступа"

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.submit_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)

    def draw(self):
        self.screen.fill(BACKGROUND)

        # Заголовок
        title = self.font.render("ПРОВЕРКА ДОСТУПА", True, TEXT)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Инструкция
        instr = self.small_font.render("Введите код:", True, (200, 200, 200))
        self.screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 170))

        # Поле ввода кода
        input_bg = pygame.Rect(WIDTH // 2 - 150, 220, 300, 80)
        pygame.draw.rect(self.screen, (30, 30, 40), input_bg, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 150), input_bg, 3, border_radius=10)

        # Отображаем код звездочками
        display_code = "•" * len(self.input_code)
        code_text = self.font.render(display_code, True, (255, 255, 255))
        self.screen.blit(code_text, (input_bg.centerx - code_text.get_width() // 2,
                                     input_bg.centery - code_text.get_height() // 2))

        if self.message:
            msg_text = self.font.render(self.message, True, (255, 0, 0))
            self.screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 360))

        self.submit_button.draw(self.screen)
        self.exit_button.draw(self.screen)

        if self.show_demo_info:
            demo_text = self.small_font.render("КОД можно получить в тг @barnaeva_m за оплату подписки", True, (150, 150, 150))
            self.screen.blit(demo_text, (WIDTH // 2 - demo_text.get_width() // 2, HEIGHT - 50))

    def run(self):
        self.clock.tick(FPS)

        if not self.handle_events():
            return False

        self.update()
        self.draw()
        pygame.display.flip()

        return True