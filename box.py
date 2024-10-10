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
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(WIDTH // 2, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    
    elapsed_time = 0       
    delay = random.choice([1000, 2000])  
    movement_distance = 100  
    distance_moved = 0       
    direction = random.choice(['up', 'down', 'none'])
    is_moving = False        

    print(f"Initial delay: {delay} ms")

    while run:
        dt = clock.tick(FPS)  
        draw(WIN, [left_paddle])

        if not is_moving:
            elapsed_time += dt
            if elapsed_time >= delay:
                
                is_moving = True
                distance_moved = 0  
                direction = random.choice(['up', 'down', 'none'])
                print(f"Starting movement: {direction}")
        else:
            
            if distance_moved < movement_distance:
                
                if direction == 'up' and left_paddle.y - left_paddle.VEL >= 0:
                    left_paddle.move(up=True)
                    distance_moved += left_paddle.VEL
                elif direction == 'down' and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
                    left_paddle.move(up=False)
                    distance_moved += left_paddle.VEL
                else:
                    print("Movement blocked or direction is 'none'")
                    
                    is_moving = False
                    elapsed_time = 0
                    delay = random.choice([1000, 2000])
            else:
                
                is_moving = False
                elapsed_time = 0  
                delay = random.choice([1000, 2000])  
                print(f"Movement complete. Next delay: {delay} ms")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
