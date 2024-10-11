import os
import pygame
import random  
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

OUTPUT_FOLDER = 'Frames'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

frame_count = 0

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

def draw(win, paddles):
    win.fill(BLACK)

    for paddle in paddles:
        paddle.draw(win)

    pygame.display.update()

def main():
    frame_count = 0
    frame_number_width = 10  # Total digits for frame number with leading zeros
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(
        WIDTH // 2, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
    )

    elapsed_time = 0
    move_time = 0
    delay = random.choice([0, 1000, 2000])
    movement_distance = 100
    distance_moved = 0
    direction = random.choice([1, -1, 0])  
    is_moving = False

    while run:
        dt = clock.tick(FPS)
        draw(WIN, [left_paddle])

        current_time = pygame.time.get_ticks()
        current_time_sec = current_time / 1000  

        if is_moving:
            current_direction = direction  
        else:
            current_direction = 0  

        frame_filename = os.path.join(
            OUTPUT_FOLDER,
            f'f{frame_count:0{frame_number_width}d}_{current_direction}.png'
        )
        pygame.image.save(WIN, frame_filename)
        frame_count += 1

        if not is_moving:
            elapsed_time += dt
            if elapsed_time >= delay:
                is_moving = True
                distance_moved = 0
                direction = random.choice([1, -1, 0]) 
        else:
            if distance_moved < movement_distance:
                if direction == 1 and left_paddle.y - left_paddle.VEL >= 0:
                    left_paddle.move(up=True)
                    distance_moved += left_paddle.VEL
                elif direction == -1 and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
                    left_paddle.move(up=False)
                    distance_moved += left_paddle.VEL
                else:
                    
                    is_moving = False
                    elapsed_time = 0
                    delay = random.choice([0, 1000, 2000])
            else:
            
                is_moving = False
                elapsed_time = 0
                delay = random.choice([0, 1000, 2000])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
