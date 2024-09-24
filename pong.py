import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7
PADDLE_OFFSET = 70  # Distance from the edge of the screen

# Ball settings
BALL_RADIUS = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong - Player on Right Side')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle positions
paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2  # Left paddle (AI)
paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2  # Right paddle (Player)

# Ball position
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# Ball speed
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Paddle 1 movement (AI controlled)
    # Simple AI: Move paddle1 towards the ball
    if paddle1_y + PADDLE_HEIGHT / 2 < ball_y and paddle1_y < HEIGHT - PADDLE_HEIGHT:
        paddle1_y += PADDLE_SPEED
    if paddle1_y + PADDLE_HEIGHT / 2 > ball_y and paddle1_y > 0:
        paddle1_y -= PADDLE_SPEED

    # Paddle 2 movement (Up and Down arrow keys)
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - PADDLE_HEIGHT:
        paddle2_y += PADDLE_SPEED

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (ball_x - BALL_RADIUS <= PADDLE_OFFSET + PADDLE_WIDTH and
        paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT):
        ball_speed_x *= -1
    if (ball_x + BALL_RADIUS >= WIDTH - PADDLE_OFFSET - PADDLE_WIDTH and
        paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    # Ball goes out of bounds (reset position)
    if ball_x < 0 or ball_x > WIDTH:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x *= -1

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles with offset
    paddle1 = pygame.draw.rect(screen, WHITE, (PADDLE_OFFSET, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    paddle2 = pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_OFFSET - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    ball = pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
