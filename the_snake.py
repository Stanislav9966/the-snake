from random import choice, randint

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка. Счет: 0.')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
# Пришлось везде добавить дефолтное значение body_color
# Так как не проходил pytest
class GameObject:
    """Базовый класс"""

    def __init__(
        self,
        body_color=None,
        taken_positions=START_POSITION
    ):
        self.position = START_POSITION
        self.body_color = body_color
        self.border_color = BORDER_COLOR
        self.taken_positions = (taken_positions)

    def draw(self):
        """Пустой метод для базового класса"""
        raise NotImplementedError('<Пустой метод для отрисовки объектов>')

    def draw_cell(self, position: tuple):
        """
        Универсальный метод для отрисовки
        одной ячейки яблока/камня
        и головы змейки
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


class Apple(GameObject):
    """Наследующий класс объект из одной клетки для яблока/камня"""

    def __init__(
            self, body_color=None,
            taken_positions=START_POSITION
    ):
        super().__init__(body_color, taken_positions)
        self.randomize_position(self.taken_positions)

    def randomize_position(self, taken_positions):
        """Метод случайной позиции яблока"""
        while True:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position_xy = (position_x, position_y)

            # Проверка на пересечение с клетками змейки и камня
            if (position_xy not in taken_positions):
                self.position = position_xy
                return position_xy

    def draw(self):
        """Метод отрисовки яблока"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Наследующий класс змейка"""

    def __init__(
        self, body_color=None,
        taken_positions=START_POSITION
    ):
        super().__init__(body_color, taken_positions)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """Метод движения змейки с проверкой на столкновения"""
        x_head, y_head = self.get_head_position()
        x_direct, y_direct = self.direction

        new_x = (x_head // GRID_SIZE + x_direct) % GRID_WIDTH
        new_y = (y_head // GRID_SIZE + y_direct) % GRID_HEIGHT
        new_head_position = (new_x * GRID_SIZE, new_y * GRID_SIZE)
        self.positions.insert(0, new_head_position)
        return new_head_position

    def reset(self):
        """
        Восстановление исходного положения и длины змейки
        при столкновении.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions[1:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.border_color, rect, 1)

#     # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Метод определения головы змейки
        для отрисовки и движения.
        """
        head_position = self.positions[0]
        return head_position

    def update_direction(self):
        """Обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция управления змейкой при движении"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, отвечающая за логику игры"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    stone = Apple(
        STONE_COLOR,
        (tuple(snake.positions) + apple.position)
    )
    score = 0

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()

        # Движение и проверка на столкновение с яблоком/камнем, изменения счета
        result_move = snake.move()
        taken_positions = (
            tuple(snake.positions)
            + apple.position + stone.position
        )
        if result_move == apple.position:
            snake.length += 1
            apple.randomize_position(taken_positions)
            score += 100
            pg.display.set_caption(f'Змейка. Счет: {score}.')
        elif result_move == stone.position:
            snake.length = 1
            snake.positions = [result_move]
            stone.randomize_position(taken_positions)
            score -= 100
            score = max(0, score)
            screen.fill(BOARD_BACKGROUND_COLOR)
            pg.display.set_caption(f'Змейка. Счет: {score}.')
        elif result_move in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(tuple(snake.positions))
            taken_positions += apple.position
            stone.randomize_position(
                tuple(snake.taken_positions) + apple.position
            )
            score = 0
            screen.fill(BOARD_BACKGROUND_COLOR)
            pg.display.set_caption(f'Змейка. Счет: {score}.')
        else:
            snake.last = snake.positions.pop()
        snake.draw()
        apple.draw()
        stone.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
