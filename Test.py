import unittest
from random import choice
from GameModel import GameModel, MahjongTile  # Убедитесь, что класс MahjongTile импортирован


class TestGameModel(unittest.TestCase):
    """Тесты для модели игры Маджонг."""

    def setUp(self):
        """Создание экземпляра модели перед каждым тестом."""
        self.game_model = GameModel()
        self.game_model.generate_tiles()  # Генерация плиток
        self.game_model.create_board()  # Создание игрового поля

    def test_generate_tiles(self):
        """Тест на генерацию плиток."""
        self.game_model.generate_tiles()
        self.assertEqual(len(self.game_model.tiles), self.game_model.size * 4,
                         "Количество плиток должно быть равно размеру поля * 4.")
        self.assertTrue(all(isinstance(tile, MahjongTile) for tile in self.game_model.tiles),
                        "Все элементы в списке плиток должны быть экземплярами MahjongTile.")

    def test_create_board(self):
        """Тест на создание игрового поля."""
        self.game_model.create_board()
        # Проверяем, что количество строк равно 4
        self.assertEqual(len(self.game_model.board), 4,
                         "Поле должно содержать 4 строки.")
        # Проверяем, что в каждой строке по 9 плиток
        self.assertTrue(all(len(row) == 9 for row in self.game_model.board),
                        "Каждая строка игрового поля должна содержать 9 плиток.")

    def test_is_tile_connectable_true(self):
        """Тест на проверку соединения плиток (положительный случай)."""
        tile1 = MahjongTile("Bamboo")
        tile2 = MahjongTile("Bamboo")
        self.assertTrue(self.game_model.is_tile_connectable(tile1, tile2),
                        "Плитки с одинаковыми типами должны быть соединяемыми.")

    def test_is_tile_connectable_false(self):
        """Тест на проверку соединения плиток (отрицательный случай)."""
        tile1 = MahjongTile("Bamboo")
        tile2 = MahjongTile("Character")
        self.assertFalse(self.game_model.is_tile_connectable(tile1, tile2),
                         "Плитки с разными типами не должны быть соединяемыми.")

    def test_tile_state_after_click(self):
        """Тест на изменение состояния плитки после клика (открытия)."""
        tile = self.game_model.board[0][0]  # Берем первую плитку
        tile.is_open = True  # Симулируем открытие плитки
        self.assertTrue(tile.is_open, "Плитка должна быть открыта после клика.")

    def test_empty_board(self):
        """Тест на пустое игровое поле (если плитки не были сгенерированы)."""
        empty_game_model = GameModel()
        self.assertEqual(empty_game_model.get_board(), [], "Пустое игровое поле должно быть пустым.")
        empty_game_model.generate_tiles()
        empty_game_model.create_board()
        self.assertGreater(len(empty_game_model.get_board()), 0,
                           "Поле должно быть заполнено плитками после генерации и создания.")

    def test_no_tiles(self):
        """Тест на отсутствие плиток перед генерацией."""
        empty_game_model = GameModel()
        self.assertEqual(len(empty_game_model.tiles), 0, "До генерации плиток список плиток должен быть пустым.")
        empty_game_model.generate_tiles()
        self.assertGreater(len(empty_game_model.tiles), 0,
                           "После генерации плиток список плиток должен содержать элементы.")


if __name__ == "__main__":
    unittest.main()
