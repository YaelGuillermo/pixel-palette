import sys
import os
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QColor, QClipboard, QImage
from PyQt5.QtCore import Qt, QTimer

SCREENSHOT_IMAGE = 'screenshot.png'
SCREENSHOT_WIDTH = 800
SCREENSHOT_HEIGHT = 400

def clear_screen():
    os.system('clear')

class MainWindow(QMainWindow):
    clear_screen()
    def __init__(self):
        super().__init__()
        self.screenshot = None
        self.zoom_factor = 1.0
        self.setWindowTitle("Pixel Palette")

        style_sheet = open('styles.css').read()
        self.setStyleSheet(style_sheet)

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
        self.color_label.setVisible(False)

        self.hexa_label = QLabel(self)
        self.hexa_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hexa_label)
        self.hexa_label.setVisible(False)

        self.color_box = QLabel(self)
        self.color_box.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.color_box)
        self.color_box.setVisible(False)  

        self.copy_rgb_button = QPushButton("Copy RGB", self)
        self.copy_rgb_button.clicked.connect(self.copy_rgb)
        self.copy_rgb_button.setVisible(False)  

        self.copy_hexa_button = QPushButton("Copy HEXA", self)
        self.copy_hexa_button.clicked.connect(self.copy_hexa)
        self.copy_hexa_button.setVisible(False) 
        '''
        self.zoom_in_button = QPushButton("+ Zoom", self)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("- Zoom", self)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        layout.addWidget(self.zoom_out_button)

        self.reset_zoom_button = QPushButton("Reset Zoom", self)
        self.reset_zoom_button.clicked.connect(self.reset_zoom)
        layout.addWidget(self.reset_zoom_button)
        '''
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_rgb_button)
        button_layout.addWidget(self.copy_hexa_button)
        layout.addLayout(button_layout)

        self.show()

    def take_screenshot(self):
        self.hide()
        QTimer.singleShot(1, self.capture_screenshot)

    def capture_screenshot(self):
        self.screenshot = pyautogui.screenshot()
        self.screenshot = self.screenshot.resize((SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
        self.screenshot.save(SCREENSHOT_IMAGE)
        pixmap = QPixmap(SCREENSHOT_IMAGE)
        self.image_label.setPixmap(pixmap)
        self.copy_rgb_button.setVisible(False)  
        self.copy_hexa_button.setVisible(False)
        self.color_label.setVisible(False)
        self.hexa_label.setVisible(False)
        self.color_box.setVisible(False)    
        self.image_label.mousePressEvent = self.get_pixel_color
        QTimer.singleShot(1, self.restore_window)
    
    def restore_window(self):
        self.show()

    def get_pixel_color(self, event):
        x = event.pos().x()
        y = event.pos().y()
        color = self.screenshot.getpixel((x, y))
        self.copy_rgb_button.setVisible(True) 
        self.copy_hexa_button.setVisible(True)
        self.color_label.setVisible(True)
        self.hexa_label.setVisible(True)
        self.color_box.setVisible(True)    
        self.color_label.setText("RGB: ({}, {}, {})".format(color[0], color[1], color[2]))
        hex_color = '#{0:02x}{1:02x}{2:02x}'.format(color[0], color[1], color[2])
        self.hexa_label.setText("HEXA: {}".format(hex_color))
        self.color_box.setStyleSheet("background-color: rgb({},{},{}); border: 0.5px solid #0F0F0F; border-radius: 5px;".format(color[0], color[1], color[2]))

    def copy_rgb(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.color_label.text())

    def copy_hexa(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.hexa_label.text())
    
    def zoom_in(self):
        self.zoom_factor += 0.1  # Aumentar el factor de escala
        self.update_image()

    def zoom_out(self):
        self.zoom_factor -= 0.1  # Reducir el factor de escala
        self.update_image()
    
    def reset_zoom(self):
        self.zoom_factor = 1.0  # Restablecer el factor de escala
        self.update_image()
    
    def update_image(self):
        if self.screenshot is not None:
            scaled_pixmap = self.screenshot.scaled(SCREENSHOT_WIDTH * self.zoom_factor, SCREENSHOT_HEIGHT * self.zoom_factor)
            self.image_label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


