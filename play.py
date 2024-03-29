import pygetwindow as gw
import pyautogui
import time

DESUME = "DeSmuME"
UP_KEY = "up"
DOWN_KEY = 'down'
RIGHT_KEY = 'right'
LEFT_KEY = 'left'
B_KEY = 'S'
A_KEY = 'D'
Y_KEY = 'A'
X_KEY = 'W'

def game_input(input_key):
	# Mimic a press, add delay to detect and register
	pyautogui.keyDown(input_key)
	time.sleep(0.05)
	pyautogui.keyUp(input_key)

def start_combo():
	# Open DeSmuME
	window_title = [title for title in gw.getAllTitles() if DESUME in title][0]
	game_window = gw.getWindowsWithTitle(window_title)[0]
	game_window.activate()
	game_input('f1')

def is_mario():
	return True

def is_baby():
	return True

def get_distance():
	return 0.0

if __name__ == '__main__':
	start_combo()
