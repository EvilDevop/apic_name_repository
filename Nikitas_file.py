import os
import sys

from PyQt5 import QtCore
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [600, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.y_mem = 228
        self.x_mem = 228

        self.initUI()
        self.map_scale = 0.001
        self.x = 55
        self.y = 55
        self.f = True

    def getImage(self):
        if self.x_coord.text() != '':
            if self.x_mem != int(self.x_coord.text()) and self.x_mem != 228 and \
                    self.y_mem != int(self.y_coord.text()) and self.y_mem != 228:
                self.f = True

            if self.f:
                self.x_mem = int(self.x_coord.text())
                self.y_mem = int(self.y_coord.text())
                self.x = int(self.x_coord.text())
                self.y = int(self.y_coord.text())
            self.f = False
            self.is_file = True
            map_request = (f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}"
                           f"&spn={str(self.map_scale)},0.01&l={self.layer}")
            response = requests.get(map_request)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)

            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.layer = 'map'
        self.is_file = False
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.x_text = QLabel('x-координата', self)
        self.x_text.move(20, 464)
        self.x_coord = QLineEdit(self)

        self.x_coord.move(100, 460)
        self.x_coord.resize(250, 23)

        self.y_text = QLabel('y-координата', self)
        self.y_text.move(20, 494)
        self.y_coord = QLineEdit(self)

        self.y_coord.move(100, 490)
        self.y_coord.resize(250, 23)
        self.get_response_button = QPushButton('Показать', self)
        self.get_response_button.move(20, 520)
        self.get_response_button.clicked.connect(self.getImage)

        self.map_button = QPushButton('схема', self)
        self.map_button.move(400, 459)
        self.map_button.clicked.connect(self.change_layer)
        self.map_button.clicked.connect(self.getImage)
        self.sat_button = QPushButton('спутник', self)
        self.sat_button.move(400, 489)
        self.sat_button.clicked.connect(self.change_layer)
        self.sat_button.clicked.connect(self.getImage)
        self.hybrid_button = QPushButton('гибрид', self)
        self.hybrid_button.move(400, 519)
        self.hybrid_button.clicked.connect(self.change_layer)
        self.hybrid_button.clicked.connect(self.getImage)

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def change_layer(self):
        if self.sender().text() == 'схема':
            self.layer = 'map'
        elif self.sender().text() == 'спутник':
            self.layer = 'sat'
        else:
            self.layer = 'skl'

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            self.map_scale += 1
            self.getImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.map_scale > 1:
                self.map_scale -= 1
            self.getImage()

        elif event.key() == QtCore.Qt.Key_D:
            self.x += 1
            self.getImage()

        elif event.key() == QtCore.Qt.Key_A:
            self.x -= 1
            self.getImage()

        elif event.key() == QtCore.Qt.Key_W:
            self.y += 1
            self.getImage()

        elif event.key() == QtCore.Qt.Key_S:
            self.y -= 1
            self.getImage()
        event.accept()

    def closeEvent(self, event):
        os.remove(self.map_file) if self.is_file else None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())