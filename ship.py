import pygame

from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, speed=0):
        super().__init__()
        self.screen = screen

        # Load image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Place ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.speed = speed

        self.center = float(self.rect.centerx)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def move_right(self):
        if self.rect.right < self.screen_rect.right:
            self.center += self.speed
            self.rect.centerx = self.center

    def move_left(self):
        if self.rect.left > 0:
            self.center -= self.speed
            self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.rect.centerx = self.center
