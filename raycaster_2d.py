import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple FPS (Raycaster)")

# Map settings (a simple grid: '1' = wall, '0' = empty space)
game_map = [
    "1111111111",
    "1000000001",
    "1011111101",
    "1000000001",
    "1111111111"
]
MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)

# Player settings
player_x = 3.0
player_y = 3.0
player_angle = 0.0  # Facing right (radians)
FOV = math.pi / 3   # 60° field of view
MOVE_SPEED = 0.05
ROT_SPEED = 0.03

clock = pygame.time.Clock()

def cast_ray(screen_x):
    """
    Cast a ray for a given screen column and return the distance to a wall.
    """
    # Determine the angle of this ray relative to the player's viewing direction
    ray_angle = player_angle - FOV / 2 + (screen_x / WIDTH) * FOV
    # Ray direction
    dx = math.cos(ray_angle)
    dy = math.sin(ray_angle)

    distance = 0.0
    hit = False
    # Increment the ray in small steps until a wall is hit or we reach a max distance.
    while not hit and distance < 20:
        distance += 0.01
        test_x = int(player_x + dx * distance)
        test_y = int(player_y + dy * distance)
        # If out of bounds, set max distance
        if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
            hit = True
            distance = 20
        elif game_map[test_y][test_x] == '1':
            hit = True
    return distance

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= ROT_SPEED
    if keys[pygame.K_RIGHT]:
        player_angle += ROT_SPEED
    if keys[pygame.K_UP]:
        new_x = player_x + math.cos(player_angle) * MOVE_SPEED
        new_y = player_y + math.sin(player_angle) * MOVE_SPEED
        if game_map[int(new_y)][int(new_x)] == '0':
            player_x = new_x
            player_y = new_y
    if keys[pygame.K_DOWN]:
        new_x = player_x - math.cos(player_angle) * MOVE_SPEED
        new_y = player_y - math.sin(player_angle) * MOVE_SPEED
        if game_map[int(new_y)][int(new_x)] == '0':
            player_x = new_x
            player_y = new_y

    # Draw ceiling (sky) and floor
    screen.fill((135, 206, 235))  # Sky blue for ceiling
    pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))  # Floor

    # Raycasting: For each vertical slice of the screen
    for x in range(WIDTH):
        distance = cast_ray(x)
        # Correct the distance for the fish-eye effect
        ray_angle = player_angle - FOV / 2 + (x / WIDTH) * FOV
        distance *= math.cos(ray_angle - player_angle)
        # Calculate wall height on screen
        if distance > 0:
            wall_height = min(int(HEIGHT / distance), HEIGHT)
        else:
            wall_height = HEIGHT
        # Determine color intensity based on distance (farther is darker)
        intensity = max(0, min(255, int(255 / (1 + distance * distance * 0.1))))
        color = (intensity, 0, 0)
        # Draw the wall slice
        pygame.draw.line(
            screen,
            color,
            (x, HEIGHT // 2 - wall_height // 2),
            (x, HEIGHT // 2 + wall_height // 2)
        )

    pygame.display.flip()
    clock.tick(60)