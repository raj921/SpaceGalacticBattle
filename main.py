
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Improved Pygame Example")

# Load images
bg_image = pygame.image.load("img.png").convert()
player_image = pygame.image.load("img_1.png").convert_alpha()
enemy_image = pygame.image.load("img_2.png").convert_alpha()

# Load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
collision_sound = pygame.mixer.Sound("collision.wav")

# Set up game clock
clock = pygame.time.Clock()

# Set up player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.right += self.speed

# Set up enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 736)
        self.rect.y = 50
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 736)
            self.rect.y = 0

# Set up bullet sprite class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

# Set up game state
class GameState:
    def __init__(self):
        self.score = 0
        self.game_over = False

    def reset(self):
        self.score = 0
        self.game_over = False

# Set up game state object
game_state = GameState()

# Set up sprite groups
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

# Create player object and add to sprite groups
player = Player(400, 500)
all_sprites.add(player)
player_sprites.add(player)

# Create enemy objects and add to sprite groups
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_state.game_over:
        # Handle shooting bullets
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if len(bullet_sprites) < 5:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)
                shoot_sound.play()

    # Check for collisions between bullets and enemies
    bullet_hits = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
    for bullet in bullet_hits.keys():
        game_state.score += 10
        collision_sound.play()

    # Check for collisions between player and enemies
    player_hits = pygame.sprite.spritecollide(player, enemy_sprites, False)
    if player_hits:
        game_state.game_over = True
        pygame.mixer.music.stop()
        collision_sound.play()
        pygame.time.delay(1000)

    # Update game state
    if game_state.game_over:
        # Display game over message
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (350, 250))

        restart_text = font.render("Press R to restart", True, (255, 0, 0))
        screen.blit(restart_text, (330, 300))

        # Restart the game when R key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state.reset()
            all_sprites.empty()
            player_sprites.empty()
            enemy_sprites.empty()
            bullet_sprites.empty()

            player = Player(400, 500)
            all_sprites.add(player)
            player_sprites.add(player)

            for _ in range(5):
                enemy = Enemy()
                all_sprites.add(enemy)
                enemy_sprites.add(enemy)

    # Draw background
    screen.blit(bg_image, (0, 0))

    # Draw sprites
    all_sprites.draw(screen)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: {}".format(game_state.score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

