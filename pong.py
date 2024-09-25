import pygame
import sys
import random

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

# Right Paddle AI toggle
RIGHT_PADDLE_AI = True  # Set to True for AI control, False for stationary paddle

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong - Lag Fix Applied')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle positions
paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2  # Left paddle (AI)
paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2  # Right paddle (Stationary or AI)

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

    # Get keys pressed (not used when paddle is stationary)
    keys = pygame.key.get_pressed()

    # Paddle 1 movement (AI controlled)
    # Simple AI: Move paddle1 towards the ball
    if paddle1_y + PADDLE_HEIGHT / 2 < ball_y and paddle1_y < HEIGHT - PADDLE_HEIGHT:
        paddle1_y += PADDLE_SPEED
    elif paddle1_y + PADDLE_HEIGHT / 2 > ball_y and paddle1_y > 0:
        paddle1_y -= PADDLE_SPEED

    # Paddle 2 movement
    if RIGHT_PADDLE_AI:
        # Move paddle2 randomly
        move = random.choice([-PADDLE_SPEED, 0, PADDLE_SPEED])
        paddle2_y += move
        # Keep paddle within screen bounds
        paddle2_y = max(0, min(paddle2_y, HEIGHT - PADDLE_HEIGHT))
    else:
        # Paddle remains stationary
        pass  # Do nothing, paddle2_y remains the same

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball_y - BALL_RADIUS <= 0:
        ball_y = BALL_RADIUS  # Reset position to prevent sticking
        ball_speed_y *= -1
    elif ball_y + BALL_RADIUS >= HEIGHT:
        ball_y = HEIGHT - BALL_RADIUS  # Reset position to prevent sticking
        ball_speed_y *= -1

    # Ball collision with left paddle (AI)
    if (ball_x - BALL_RADIUS <= PADDLE_OFFSET + PADDLE_WIDTH and
        paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT):
        ball_x = PADDLE_OFFSET + PADDLE_WIDTH + BALL_RADIUS  # Move ball outside paddle
        ball_speed_x *= -1

    # Ball collision with right paddle (Stationary or AI)
    if RIGHT_PADDLE_AI:
        if (ball_x + BALL_RADIUS >= WIDTH - PADDLE_OFFSET - PADDLE_WIDTH and
            paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
            ball_x = WIDTH - PADDLE_OFFSET - PADDLE_WIDTH - BALL_RADIUS  # Move ball outside paddle
            ball_speed_x *= -1
    else:
        # Skip collision with stationary paddle to prevent lag
        pass

    # Ball goes out of bounds (reset position)
    if ball_x < 0 or ball_x > WIDTH:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = BALL_SPEED_X * (-1 if ball_speed_x < 0 else 1)
        ball_speed_y = BALL_SPEED_Y * (-1 if random.choice([True, False]) else 1)

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles with offset
    paddle1 = pygame.draw.rect(screen, WHITE, (PADDLE_OFFSET, int(paddle1_y), PADDLE_WIDTH, PADDLE_HEIGHT))
    if RIGHT_PADDLE_AI or True:  # Always draw the right paddle for consistency
        paddle2 = pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_OFFSET - PADDLE_WIDTH, int(paddle2_y), PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    ball = pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
