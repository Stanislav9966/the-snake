from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка. Счет: 0.')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс"""

    def __init__(self):
        self.position = START_POSITION
        self.body_color = None

    def draw(self):
        """Пустой метод для базового класса"""
        pass


class Apple(GameObject):
    """Наследующий класс яблоко"""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions=(), stone_position=None):
        """Метод случайной позиции яблока"""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position_xy = (position_x, position_y)

            # Проверка на пересечение с клетками змейки и камня
            if (
                position_xy not in snake_positions
                and position_xy != stone_position
            ):
                self.position = position_xy
                return position_xy

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Наследующий класс яблоко"""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = STONE_COLOR

    def randomize_position(self, snake_positions=(), apple_position=None):
        """Метод случайной позиции камня"""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position_xy = (position_x, position_y)

            # Проверка на пересечение с клетками змейки и яблока
            if (
                position_xy not in snake_positions
                and position_xy != apple_position
            ):
                self.position = position_xy
                return position_xy

    def draw(self):
        """Метод отрисовки камня"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Наследующий класс змейка"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [START_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def move(self, apple_position, stone_position):
        """Метод движения змейки с проверкой на столкновения"""
        head_position = self.get_head_position()
        new_direct = list(self.direction)

        new_x = (head_position[0] // GRID_SIZE + new_direct[0]) % GRID_WIDTH
        new_y = (head_position[1] // GRID_SIZE + new_direct[1]) % GRID_HEIGHT
        new_head_position = (new_x * GRID_SIZE, new_y * GRID_SIZE)

        # Проверка на столкновения с яблоком/камнем/самоукус
        if new_head_position == apple_position:
            self.positions.insert(0, new_head_position)
            self.length += 1
            result = 'apple'
        elif new_head_position == stone_position:
            self.length -= 1
            self.positions = [new_head_position]
            result = 'stone'
        elif new_head_position in self.positions[1:]:
            self.reset()
            result = 'bite'
        else:
            self.positions.insert(0, new_head_position)
            self.last = self.positions.pop()
            result = 'move'
        return result

    def reset(self):
        """
        Восстановление исходного положения и длины змейки
        при столкновении.
        """
        self.length = 1
        self.positions = [START_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Метод определения головы змейки
        для отрисовки и движения.
        """
        head_position = self.positions[0]
        return list(head_position)

    def update_direction(self):
        """Обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция управления змейкой при движении"""
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


def main():
    """Основная функция, отвечающая за логику игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    stone = Stone()
    score = 0
    # Проверка на пересечение клеток в начале игры
    apple.randomize_position(snake.positions, stone.position)
    stone.randomize_position(snake.positions, apple.position)

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()

        # Результат проверки для нового положения яблока/камня изменения счета
        result_move = snake.move(apple.position, stone.position)
        if result_move == 'apple':
            apple.randomize_position(snake.positions, stone.position)
            score += 100
            pygame.display.set_caption(f'Змейка. Счет: {score}.')
        elif result_move == 'stone':
            stone.randomize_position(snake.positions, apple.position)
            score -= 100
            score = max(0, score)
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.set_caption(f'Змейка. Счет: {score}.')
        elif result_move == 'bite':
            apple.randomize_position(snake.positions, stone.position)
            stone.randomize_position(snake.positions, apple.position)
            score = 0
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.set_caption(f'Змейка. Счет: {score}.')

        snake.draw()
        apple.draw()
        stone.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
