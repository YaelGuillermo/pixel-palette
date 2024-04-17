import sys
import os
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QColor, QClipboard
from PyQt5.QtCore import Qt

SCREENSHOT_IMAGE = 'screenshot.png'
SCREENSHOT_WIDTH = 500
SCREENSHOT_HEIGHT = 400

def clear_screen():
    os.system('clear')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.button = QPushButton("Take Screenshot", self)
        self.button.clicked.connect(self.take_screenshot)
        layout.addWidget(self.button, alignment=Qt.AlignHCenter)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.color_label = QLabel(self)
        self.color_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.color_label)

        self.hexa_label = QLabel(self)
        self.hexa_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hexa_label)

        self.color_box = QLabel(self)
        self.color_box.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.color_box)

        self.copy_rgb_button = QPushButton("Copy RGB", self)
        self.copy_rgb_button.clicked.connect(self.copy_rgb)
        self.copy_rgb_button.setVisible(False)  # Invisible por defecto
        self.copy_hexa_button = QPushButton("Copy HEXA", self)
        self.copy_hexa_button.clicked.connect(self.copy_hexa)
        self.copy_hexa_button.setVisible(False)  # Invisible por defecto

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_rgb_button)
        button_layout.addWidget(self.copy_hexa_button)
        layout.addLayout(button_layout)

        self.show()

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.resize((SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
        screenshot.save(SCREENSHOT_IMAGE)
        pixmap = QPixmap(SCREENSHOT_IMAGE)
        self.image_label.setPixmap(pixmap)
        self.button.hide()  # Ocultar el botón después de tomar la captura
        self.copy_rgb_button.setVisible(True)  # Mostrar botón de copiar RGB
        self.copy_hexa_button.setVisible(True)  # Mostrar botón de copiar HEXA
        self.image_label.mousePressEvent = self.get_pixel_color

    def get_pixel_color(self, event):
        x = event.pos().x()
        y = event.pos().y()
        screenshot = pyautogui.screenshot(region=(self.x() + x, self.y() + y, 1, 1))
        color = screenshot.getpixel((0, 0))
        self.color_label.setText("RGB: ({}, {}, {})".format(color[0], color[1], color[2]))
        hex_color = '#{0:02x}{1:02x}{2:02x}'.format(color[0], color[1], color[2])
        self.hexa_label.setText("HEXA: {}".format(hex_color))
        self.color_box.setStyleSheet("background-color: rgb({},{},{});".format(color[0], color[1], color[2]))

    def copy_rgb(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.color_label.text())

    def copy_hexa(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.hexa_label.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


