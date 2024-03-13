import sys
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject представляет объекты на игровом поле."""

    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки"""
        pass

    def draw_rect(self, position):
        """Метод для отрисовки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake для описания змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self):
        """Метод для описания сменны движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для описания движения змеи"""
        head_position = self.get_head_position()
        new_head = (
            head_position[0] + GRID_SIZE * self.direction[0],
            head_position[1] + GRID_SIZE * self.direction[1],
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def get_head_position(self):
        """Метод для получения головы змеи."""
        return self.positions[0]

    def reset(self):
        """Метод для перезапуска игры."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Метод для отрисовки змеи."""
        for position in self.positions[:-1]:
            self.draw_rect(position)
        self.draw_rect(self.get_head_position())


class Apple(GameObject):
    """Класс Apple для описания обьекта яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, snake_pos=[SCREEN_CENTER]):
        """Определение положения яблока."""
        while self.position in snake_pos:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )

    def draw(self):
        """Метод для отрисовки яблока"""
        self.draw_rect(self.position)


def handle_keys(game_object):
    """Метод обрабатывающий действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция для запуска игры"""
    snake = Snake()
    apple = Apple()
    pygame.init()
    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if (
            not (0 <= snake.get_head_position()[0] < GRID_WIDTH * GRID_SIZE)
            or not (0 <= snake.get_head_position()[1] < GRID_HEIGHT * GRID_SIZE)
            or any(
                snake.get_head_position() in segment for segment in snake.positions[1:]
            )
        ):
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
