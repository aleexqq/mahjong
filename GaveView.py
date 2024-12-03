import sys
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, \
    QGraphicsSimpleTextItem
from GameModel import GameModel, MahjongTile


class TileItem(QGraphicsRectItem):
    """Графический элемент для плитки Маджонга."""

    current_z = 0

    def __init__(self, tile, x, y, size=80):
        super().__init__(QRectF(0, 0, size, size))
        self.tile = tile

        # Установка позиции плитки на сцене
        self.setPos(x, y)

        # Фон плитки
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.default_pen = QPen(Qt.black)
        self.setPen(self.default_pen)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable)

        self.text_item = QGraphicsSimpleTextItem(str(self.tile.tile_type), self)
        self.text_item.setPos(10, 30)  # Относительные координаты внутри плитки
        self.text_item.setFont(QFont('Arial', 8))
        self.text_item.setBrush(QBrush(QColor(0, 0, 0)))

    def mousePressEvent(self, event):
        """Обработка клика по плитке."""
        super().mousePressEvent(event)
        self.tile.is_open = True  # Открываем плитку
        print(f"Tile clicked: {self.tile}")  # Выводим информацию о плитке

    def select_tile(self):
        """Изменение внешнего вида при выборе плитки."""
        # Поднять плитку по Z
        TileItem.current_z += 1
        self.setZValue(TileItem.current_z)

        dashed_pen = QPen(Qt.black)
        dashed_pen.setStyle(Qt.DashLine)
        self.setPen(dashed_pen)

    def deselect_tile(self):
        """Восстановление внешнего вида при снятии выбора."""
        self.setZValue(0)

        self.setPen(self.default_pen)


class GameView(QMainWindow):
    """Представление игры Маджонг с использованием QGraphicsScene."""

    def __init__(self, game_model):
        super().__init__()
        self.setWindowTitle('Mahjong Connect')
        self.setGeometry(100, 100, 800, 600)

        self.game_model = game_model
        self.selected_tile = None
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса с использованием QGraphicsScene."""
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.scene.selectionChanged.connect(self.on_selection_changed)

        self.create_board()

    def create_board(self):
        """Отображение плиток на графической сцене."""
        board = self.game_model.get_board()
        tile_size = 80

        for row_idx, row in enumerate(board):
            for col_idx, tile in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                tile_item = TileItem(tile, x, y, tile_size)
                self.scene.addItem(tile_item)

    def on_selection_changed(self):
        """Обработка изменения выбора плиток."""
        selected_items = self.scene.selectedItems()
        if selected_items:
            new_selected_tile = selected_items[0]
            if self.selected_tile is not None and self.selected_tile != new_selected_tile:
                self.selected_tile.deselect_tile()
                self.selected_tile.setSelected(False)

            if self.selected_tile != new_selected_tile:
                self.selected_tile = new_selected_tile
                self.selected_tile.select_tile()
        else:
            if self.selected_tile is not None:
                self.selected_tile.deselect_tile()
                self.selected_tile = None

    def update_view(self):
        """Обновление состояния отображения."""
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Инициализация модели игры
    game_model = GameModel()
    game_model.generate_tiles()
    game_model.create_board()

    # Создание и отображение вида игры
    game_view = GameView(game_model)
    game_view.show()

    sys.exit(app.exec_())
