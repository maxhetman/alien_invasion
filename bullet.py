import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Create bullet and set its position
        self.rect = pygame.Rect(0, 0,
            settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's position as float value
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

