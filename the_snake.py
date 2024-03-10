from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.


# Класс GameObject
class GameObject:
    """Класс GameObject представляет объекты на игровом поле."""

    # Метод __init__ класса GameObject
    def __init__(self, position=(320, 240), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    # Метод draw класса GameObject
    def draw(self, surface):
        """Метод draw для отрисовки обьектов."""
        pass


# Класс Snake наследуемый от GameObject
class Snake(GameObject):
    """Класс Snake для описания змейки."""

    def __init__(self):
        super().__init__()  # Вызов конструктора родительского класса
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    # Метод update_diretion класса Snake
    def update_direction(self):
        """Метод для описания сменны движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод move обьекта Snake
    def move(self):
        """Метод для описания движения змеи."""
        new_head = (
            self.positions[0][0] + GRID_SIZE * self.direction[0],
            self.positions[0][1] + GRID_SIZE * self.direction[1],
        )
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH * GRID_SIZE
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT * GRID_SIZE
        ):  # Проверка столкновения со стеной
            self.reset()
        elif any(
            new_head in segment for segment in self.positions[1:]
        ):  # Проверка столкновения с самой собой
            self.reset()
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    # Метод для получения головы змеи
    def get_head_position(self):
        """Метод для получения головы змеи."""
        return self.positions[0]

    # Метод для перезапуска игры при столкновении с самим собой
    def reset(self):
        """Метод для перезапуска игры."""
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = RIGHT
        self.next_direction = None

    # Метод draw класса Snake
    def draw(self, surface):
        """Метод для отрисовки змеи."""
        for position in self.positions[:-1]:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)


# Класс Apple наследуемый от GameObject
class Apple(GameObject):
    """Класс Apple для описания обьекта яблока."""

    # Метод __init__ класса Apple
    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position()

    # Метод randomize_pozition класса Apple
    def randomize_position(self):
        """Метод определяющий положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    # Метод draw класса Apple
    def draw(self, surface):
        """Метод отрисовки яблока."""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Метод обрабатывающий действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Функция main
def main():
    """Функция для запуска игры"""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        for position in snake.positions[1:]:
            if position == snake.get_head_position():
                snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
