import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen_width, speed):
        super().__init__()
        self.image = pygame.image.load(
            './graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.screen_width = screen_width
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

    def shoot(self):
        print("shoot")

    def recharge(self):
        if not self.ready:
            current_laser_time = pygame.time.get_ticks()
            if current_laser_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif pressed_keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if pressed_keys[pygame.K_SPACE] and self.ready:
            self.shoot()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def constraint(self):
        if self.rect.right >= self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left <= 0:
            self.rect.left = 0

    def update(self):
        self.move()
        self.constraint()
        self.recharge()
