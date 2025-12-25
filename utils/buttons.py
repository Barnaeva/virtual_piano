import pygame
from utils.config import SIZE_TEXT, FONT


class ImageButton:
    def __init__(self, x, y, width, height, text=None, color=None, hover_color=None,
                 sound_path=None, icon=None, icon_size=None):
        """
        Улучшенная кнопка с поддержкой иконок.

        Параметры:
        - text: текст кнопки (может быть None если только иконка)
        - color: цвет фона (может быть None если только иконка)
        - icon: объект pygame.Surface с иконкой
        - icon_size: размер иконки (ширина, высота)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color if hover_color else color
        self.icon = icon
        self.icon_size = icon_size or (height - 10, height - 10)

        self.rect = pygame.Rect(x, y, width, height)
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

        # Масштабируем иконку если нужно
        if self.icon and self.icon_size:
            self.icon = pygame.transform.smoothscale(self.icon, self.icon_size)

    def set_icon(self, icon, size=None):
        """Устанавливает или меняет иконку кнопки"""
        self.icon = icon
        if size:
            self.icon_size = size
        if self.icon and self.icon_size:
            self.icon = pygame.transform.smoothscale(self.icon, self.icon_size)

    def set_text(self, text):
        """Меняет текст кнопки"""
        self.text = text

    def draw(self, screen):
        # Рисуем прямоугольник с цветом если он указан
        if self.color:
            current_color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(screen, current_color, self.rect, border_radius=12)

            # Добавляем обводку для красоты
            border_color = (min(current_color[0] + 30, 255),
                            min(current_color[1] + 30, 255),
                            min(current_color[2] + 30, 255))
            pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=12)

        # Если есть иконка, рисуем её
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)

            # Если есть текст, смещаем иконку влево
            if self.text:
                icon_rect.x = self.rect.x + 10
                icon_rect.centery = self.rect.centery

            screen.blit(self.icon, icon_rect)

        # Рисуем текст если есть
        if self.text:
            font = pygame.font.SysFont(FONT, SIZE_TEXT)
            text_surface = font.render(self.text, True, (255, 255, 255))

            # Позиционируем текст
            if self.icon:
                # Если есть иконка, текст справа от неё
                text_x = self.rect.x + (self.icon_size[0] if self.icon else 0) + 20
                text_rect = text_surface.get_rect(midleft=(text_x, self.rect.centery))
            else:
                # Если нет иконки, текст по центру
                text_rect = text_surface.get_rect(center=self.rect.center)

            screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            return True
        return False