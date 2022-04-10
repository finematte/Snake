import pygame
import math
import random
import time
import sys

# CONSTANTS
WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = WIDTH // PIXELS

# COLORS
BG1 = (156, 210, 54)
BG2 = (147, 203, 57)
RED = (255, 0, 0)
BLUE = (0, 0, 50)


class Snake:
    def __init__(self):
        self.color = BLUE
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.state = "STOP"  # STOP, UP, DOWN, RIGHT,

    def move_head(self):
        if self.state == "UP":
            self.headY -= PIXELS
        elif self.state == "DOWN":
            self.headY += PIXELS
        elif self.state == "LEFT":
            self.headX -= PIXELS
        elif self.state == "RIGHT":
            self.headX += PIXELS

    def move_body(self):
        if len(self.bodies) > 0:
            for i in range(len(self.bodies) - 1, -1, -1):
                if i == 0:
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    self.bodies[i].posX = self.bodies[i - 1].posX
                    self.bodies[i].posY = self.bodies[i - 1].posY

    def add_body(self):
        body = Body(BLUE, self.headX, self.headY)
        self.bodies.append(body)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.headX, self.headY, PIXELS, PIXELS))
        if len(self.bodies) > 0:
            for body in self.bodies:
                body.draw(surface)

    def die(self):
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies.clear()
        self.state = "STOP"


class Apple:
    def __init__(self):
        self.color = RED
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))


class Background:
    def draw(self, surface):
        surface.fill(BG1)
        counter = 0

        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    pygame.draw.rect(surface, BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                if col != SQUARES - 1:
                    counter += 1


class Collision:

    def between_snake_and_apple(self, snake, apple):
        distance = math.sqrt(math.pow((snake.headX - apple.posX), 2) + math.pow((snake.headY - apple.posY), 2))
        return distance < PIXELS

    def between_snake_and_walls(self, snake):
        if snake.headX < 0 or snake.headX > WIDTH - PIXELS or snake.headY < 0 or snake.headY > HEIGHT - PIXELS:
            return True
        return False

    def between_head_and_body(self, snake):
        for body in snake.bodies:
            distance = math.sqrt(math.pow((snake.headX - body.posX), 2) + math.pow((snake.headY - body.posY), 2))
            if distance < PIXELS:
                return True
        return False


class Body:
    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    # OBJECTS
    apple = Apple()
    snake = Snake()
    background = Background()
    collision = Collision()

    # Updating screen
    clock = pygame.time.Clock()
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, 150)

    # Main loop
    while True:
        background.draw(screen)
        apple.draw(screen)
        snake.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == screen_update:
                if collision.between_snake_and_apple(snake, apple):
                    apple.spawn()
                    snake.add_body()
                snake.move_body()
                snake.move_head()
                if collision.between_snake_and_walls(snake):
                    snake.die()
                    apple.spawn()
                if collision.between_head_and_body(snake):
                    snake.die()
                    apple.spawn()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.state != "DOWN":
                        snake.state = "UP"
                if event.key == pygame.K_DOWN:
                    if snake.state != "UP":
                        snake.state = "DOWN"
                if event.key == pygame.K_LEFT:
                    if snake.state != "RIGHT":
                        snake.state = "LEFT"
                if event.key == pygame.K_RIGHT:
                    if snake.state != "LEFT":
                        snake.state = "RIGHT"
                if event.key == pygame.K_q:
                    sys.exit()

        pygame.display.update()
        clock.tick(60)
