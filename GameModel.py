import random


class MahjongTile:
    """Представление одной плитки Маджонга."""

    def __init__(self, tile_type):
        self.tile_type = tile_type  # Тип плитки (например, цифры или символы)
        self.is_open = False  # Плитка еще не открыта

    def __repr__(self):
        return f"Tile({self.tile_type})"


class GameModel:
    """Модель игры Маджонг."""

    def __init__(self, size=9):
        self.size = size  # Размер поля
        self.tiles = []  # Список плиток
        self.board = []  # Игровое поле (матрица)

    def generate_tiles(self):
        """Генерация плиток для игры."""
        tile_types = ["Bamboo", "Character", "Circle", "Dragon"]  # Пример типов плиток
        self.tiles = [MahjongTile(random.choice(tile_types)) for _ in range(self.size * 4)]  # Плиток в 4 раза больше

    def create_board(self):
        """Создание игрового поля."""
        self.board = [self.tiles[i:i + self.size] for i in range(0, len(self.tiles), self.size)]

    def is_tile_connectable(self, tile1, tile2):
        """Проверка возможности соединения двух плиток."""
        # Простая проверка на одинаковый тип плиток.
        return tile1.tile_type == tile2.tile_type

    def get_board(self):
        """Получение текущего состояния поля."""
        return self.board
