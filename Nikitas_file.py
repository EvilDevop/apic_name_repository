import os
import sys

from PyQt5 import QtCore
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [600, 700]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.y_mem = 228
        self.x_mem = 228
        self.dict_but = {1060: 65, 1062: 87, 1042: 68, 1067: 83}
        self.initUI()
        self.map_scale = 0.001
        self.x = 55
        self.y = 55
        self.f = True

    def getImage(self, toponym_coordinates=None):
        if self.x_coord.text() != '' or toponym_coordinates is not None:
            if toponym_coordinates:
                self.x = eval(toponym_coordinates.split()[0])
                self.y = eval(toponym_coordinates.split()[1])
                self.x_coord.setText(str(self.x))
                self.y_coord.setText(str(self.y))
            if self.x_mem != eval(self.x_coord.text()) and self.x_mem != 228 and \
                    self.y_mem != eval(self.y_coord.text()) and self.y_mem != 228:
                self.f = True

            if self.f:
                self.x_mem = eval(self.x_coord.text())
                self.y_mem = eval(self.y_coord.text())
                self.x = eval(self.x_coord.text())
                self.y = eval(self.y_coord.text())
            self.f = False
            self.is_file = True
            if toponym_coordinates:
                map_request = (f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}"
                               f"&spn={str(self.map_scale)},0.01&l={self.layer}&pt="
                               f"{self.x},{self.y},pmrdm&amp")
            else:
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

    def find_toponym(self):
        geocoder_request = (f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="
                            f"{self.toponym_edit.text()}&format=json")
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coordinates = toponym["Point"]["pos"]
            self.getImage(toponym_coordinates)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

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

        self.toponym_edit = QLineEdit(self)
        self.toponym_edit.move(103, 570)
        self.toponym_edit.resize(300, 23)
        self.toponym_text = QLabel('поиск объекта', self)
        self.toponym_text.move(20, 574)
        self.search_button = QPushButton('Поиск', self)
        self.search_button.move(425, 569)
        self.search_button.clicked.connect(self.find_toponym)

    def change_layer(self):
        if self.sender().text() == 'схема':
            self.layer = 'map'
        elif self.sender().text() == 'спутник':
            self.layer = 'sat'
        else:
            self.layer = 'sat,skl'

    def keyPressEvent(self, event):
        a = event.key()
        if a in self.dict_but.keys():
            a = self.dict_but[a]
        if a == QtCore.Qt.Key_PageUp:
            self.map_scale += 1
            self.getImage()
        elif a == 16777220:
            self.getImage()
        elif a == QtCore.Qt.Key_PageDown:
            if self.map_scale > 1:
                self.map_scale -= 1
            self.getImage()

        elif a == QtCore.Qt.Key_D:
            self.x += 1
            self.getImage()

        elif a == QtCore.Qt.Key_A:
            self.x -= 1
            self.getImage()

        elif a == QtCore.Qt.Key_W:
            self.y += 1
            self.getImage()

        elif a == QtCore.Qt.Key_S:
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