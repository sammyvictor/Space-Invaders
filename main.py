import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()  # pylint: disable=no-member

# Create gaming screen
screen = pygame.display.set_mode((800, 600))

# Screen Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Set background image
background_image = pygame.image.load('background.png')

# Add background music
mixer.music.load('background.wav')
mixer.music.play(-1)


# Player
player_image = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0


def player(x, y):
    screen.blit(player_image, (x, y))


# Enemies
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(80)


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


# Bullet
# Bullet state ("ready") - means it is ready to be fired
# Bullet state ("fire") - means it has been fired
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


# Collison function - between enemy and bullet
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Calculating distace between bullet and enemy
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2)) +
                         (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


score_value = 0
score_x = 10
score_y = 10
# plint : disable = no-member
score_font = pygame.font.Font('freesansbold.ttf', 24)


def score_display(x, y):
    score = score_font.render(
        "Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Handling high score
try:
    with open('high_score.txt', 'r') as high_score_file:
        high_score_content = high_score_file.read().strip()
        high_score_value = int(high_score_content.split('=')[1].strip())
except (FileNotFoundError, IndexError, ValueError):
    # If the file is missing or the content is invalid, initialize high score to 0
    high_score_value = 0
    with open('high_score.txt', 'w') as high_score_file:
        high_score_file.write("HighScore = 0")


def high_score_display(x, y):
    high_score = score_font.render(
        "HighScore :" + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score, (x, y))


def update_high_score():
    """Update the high score if the current score exceeds it."""
    global high_score_value
    if score_value > high_score_value:
        high_score_value = score_value
        with open('high_score.txt', 'w') as high_score_file:
            high_score_file.write(f"HighScore = {high_score_value}")


# Dislay game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# Game loop
running = True
while running:

    # Add background color - uses RGB tuple
    screen.fill((0, 0, 0))
    # Display background image
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        # Close the game window when the close button is pressed
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            running = False

        # Check if the keystrokes is left or right
        if event.type == pygame.KEYDOWN:  # pylint: disable = no-member
            if event.key == pygame.K_LEFT:  # pylint: disable = no-member
                player_x_change = -4
            if event.key == pygame.K_RIGHT:  # pylint: disable = no-member
                player_x_change = 4
            # Put fire bullet using space bar
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # pylint: disable = no-member
                mixer.Sound('laser.wav').play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        # Check if the keystroke is released
        if event.type == pygame.KEYUP:  # pylint: disable = no-member
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # pylint: disable = no-member
                player_x_change = 0

    # Created boundaries to ensure the player does not go beyond the screen dimensions
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    player(player_x, player_y)

    # Created boundaries to ensure the enemy does not go beyond the screen dimensions
    # Added y-axis movement for the enemy
    for i in range(num_of_enemies):
        # Game over functionality
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -2
            enemy_y[i] += enemy_y_change[i]
        enemy(enemy_x[i], enemy_y[i], i)

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            mixer.Sound('explosion.wav').play()
            bullet_state = "ready"
            bullet_y = 480
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
            update_high_score()

    # Bullet movement when fired
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = 480

    score_display(score_x, score_y)
    high_score_display(10, 40)

    pygame.display.update()
