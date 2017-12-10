import pygame

import game_functions as gf
from game_settings import GameSettings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # Init game and create screen object
    pygame.init()
    settings = GameSettings()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    play_btn = Button(screen)
    stats = GameStats(settings)
    sb = ScoreBoard(settings, screen, stats)
    ship = Ship(screen, settings.ship_speed)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    # Start main loop for the game
    while True:
        gf.check_events(ship, bullets, settings, screen, stats, play_btn, aliens, sb)

        if stats.game_active:
            gf.update_bullets(settings, screen, ship, aliens, bullets, sb, stats)
            gf.update_aliens(settings, stats, screen, ship, aliens, bullets, sb)

        gf.update_screen(settings, screen, stats, ship, bullets, aliens, play_btn, sb)


run_game()


