import pygame
import sys
import obstacle
import random
from laser import Laser
from player import Player
from alien import Alien, Extra


class Game:
    def __init__(self):
        # player setup
        player_sprite = Player(
            (screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health system
        self.lives = 3
        self.lives_image = pygame.image.load(
            './graphics/player.png').convert_alpha()
        self.lives_x_start_pos = screen_width - \
            (self.lives_image.get_size()[0]*2 + 20)
        self.score = 0
        self.font = pygame.font.Font('./font/Pixeled.ttf', 20)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * (screen_width / self.obstacle_amount)
            for num in range(self.obstacle_amount)
        ]
        self.create_multiple_blocks(
            x_start=screen_width/15,
            y_start=480,
            offset=self.obstacle_x_positions
        )

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_x_direction = 1
        self.alien_setup(rows=6, cols=8)

        # extra alien setup
        self.extra_alien = pygame.sprite.GroupSingle()
        self.extra_alien_spawn_time = random.randint(400, 800)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(
                        x, y, self.block_size, (241, 79, 80))
                    self.blocks.add(block)

    def create_multiple_blocks(self, x_start, y_start, offset):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
            offset_x += 90

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, offset_x=70, offset_y=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + offset_x
                y = row_index * y_distance + offset_y

                if row_index == 0:
                    alien_sprite = Alien(x, y, 'yellow')
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien(x, y, 'green')
                else:
                    alien_sprite = Alien(x, y, 'red')
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_x_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_x_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self, y_distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += y_distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, screen_height, 6)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_alien_spawn_time -= 1
        if self.extra_alien_spawn_time <= 0:
            extra_alien_sprite = Extra(
                random.choice(['right', 'left']), screen_width)
            self.extra_alien.add(extra_alien_sprite)
            self.extra_alien_spawn_time = random.randint(400, 800)

    def collison_checks(self):
        # players Laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    break
                alien_hit = pygame.sprite.spritecollide(
                    laser, self.aliens, True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                    laser.kill()
                    break
                if pygame.sprite.spritecollide(laser, self.extra_alien, True):
                    self.score += 500
                    laser.kill()
                    break
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.lives_x_start_pos + \
                (live * self.lives_image.get_size()[0] + 10)
            screen.blit(self.lives_image, (x, 8))

    def display_score(self):
        score_text = self.font.render(
            f'Score: {self.score}', False, 'white')
        score_rect = score_text.get_rect(topleft=(10, -10))
        screen.blit(score_text, score_rect)

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra_alien.update()

        self.aliens.update(self.alien_x_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collison_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra_alien.draw(screen)
        self.display_lives()
        self.display_score()
        # update all sprite groups
        # draw all sprite groups


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
