import os
import pyautogui

SCREENSHOT_IMAGE = 'screenshot.png'

def clear_screen():
    os.system('clear')

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_IMAGE)

def select_coordinates():
    print("Move your mouse over the screenshot and press Ctrl + C when you're ready to select the pixel.")
    try:
        pyautogui.displayMousePosition()
    except KeyboardInterrupt:
        pass

def main():
    clear_screen()
    take_screenshot()
    select_coordinates()

if __name__ == "__main__":
    main()

