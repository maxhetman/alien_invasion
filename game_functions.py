import sys
import pygame

from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep


def check_events(ship, bullets, settings, screen, stats, play_btn, aliens, sb):
    # Check for keyboard and mouse input
    check_controls_input(ship)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, settings, screen, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, play_btn, ship, aliens, bullets, mouse_x, mouse_y, sb)


def check_play_button(settings, screen, stats, play_btn, ship, aliens, bullets, mouse_x, mouse_y, sb):
    """Start a new game when player clicks 'Play'"""
    button_clicked = play_btn.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def check_controls_input(ship):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.move_left()
    if keys[pygame.K_RIGHT]:
        ship.move_right()


def update_bullets(settings, screen, ship, aliens, bullets, sb, stats):
    """Update position of bullets and get rid of old bullets"""
    # Update position
    bullets.update()

    # Get rid of bullets that are out of screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_aliens_collisions(settings, screen, ship, aliens, bullets, sb, stats)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_aliens_collisions(settings, screen, ship, aliens, bullets, sb, stats):
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If fleet is destroyed we start new level
        bullets.empty()

        settings.increase_speed()
        ship.speed = settings.ship_speed

        stats.level += 1
        sb.prep_level()

        create_fleet(settings, screen, ship, aliens)


def update_aliens(settings, stats, screen, ship, aliens, bullets, sb):
    """Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Check alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets, sb)

    # Check for aliens hitting bottom of the screen
    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb)


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this same way as if ship got hit
            ship_hit(settings, stats, screen, ship, aliens, bullets, sb)
            break


def ship_hit(settings, stats, screen, ship, aliens, bullets, sb):
    # Pause
    sleep(0.5)
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)




def check_fleet_edges(settings, aliens):
    """Respond if any aliens have reached edge"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """Drop fleet and change it's direction"""
    for alien in aliens:
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_keydown_event(event, settings, screen, ship, bullets):
    if event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        # Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Get number of rows and number of aliens in one row
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    # Create aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def create_alien(settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the row.
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number + randint(-15, 15)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + alien.rect.height * 2 * row_number
    aliens.add(alien)


def get_number_aliens_x(settings, alien_width):
    """Determines number of aliens in one row"""
    available_space_x = settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = settings.screen_height -  3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_screen(settings, screen,stats, ship, bullets, aliens, play_btn, scoreboard):
    screen.fill(settings.bg_color)

    # Redraw all objects on screen
    scoreboard.show_score()

    if stats.game_active:
        ship.blitme()
        aliens.draw(screen)
        for bullet in bullets:
            bullet.draw_bullet()

    if not stats.game_active:
        play_btn.draw_button()

    # Make most recently drawn screen visible
    pygame.display.flip()
