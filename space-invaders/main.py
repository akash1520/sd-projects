import pygame
import sys
import obstacle
from player import Player
from alien import Alien


class Game:
    def __init__(self):
        # player setup
        player_sprite = Player(
            (screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

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
        self.alien_x_direction = 1
        self.alien_setup(rows=6, cols=8)

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
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_x_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, y_distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += y_distance

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_x_direction)
        self.alien_position_checker()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        # update all sprite groups
        # draw all sprite groups


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
