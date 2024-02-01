import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [600, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        self.is_file = True
        map_request = (f"http://static-maps.yandex.ru/1.x/?ll={self.x_coord.text()},{self.y_coord.text()}"
                       f"&spn=0.002,0.002&l=map")
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

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def closeEvent(self, event):
        os.remove(self.map_file) if self.is_file else None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())