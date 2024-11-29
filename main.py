import random
import pygame

# Initialize pygame
pygame.init()  # pylint: disable = no-member

# Create game window
screen = pygame.display.set_mode((800, 600))

# Set title and Icon
pygame.display.set_caption("Space Invader")
icon_image = pygame.image.load('ufo.png')
pygame.display.set_icon(icon_image)

# Player
player_image = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0


def player(x, y):
    screen.blit(player_image, (x, y))


# Enemy
enemy_image = pygame.image.load('enemy.png')
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)


def enemy(x, y):
    screen.blit(enemy_image, (x, y))


# Create the game loop
running = True
while running:
    for event in pygame.event.get():
        # End the game loop when close button is clicked
        if event.type == pygame.QUIT:  # pylint: disable = no-member
            running = False
        # Movement of the player using arrow keys
        if event.type == pygame.KEYDOWN:  # pylint: disable = no-member
            if event.key == pygame.K_LEFT:  # pylint: disable = no-member
                player_x_change = -0.5
            elif event.key == pygame.K_RIGHT:  # pylint: disable = no-member
                player_x_change = 0.5
        if event.type == pygame.KEYUP:  # pylint: disable = no-member
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # pylint: disable = no-member
                player_x_change = 0

    # Set background color
    screen.fill((128, 128, 128))
    # Move the player left/right
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    # Add player to screen
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    pygame.display.update()
