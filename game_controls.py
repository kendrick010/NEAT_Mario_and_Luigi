import pygetwindow as gw
import pyautogui
import time

DESUME = "DeSmuME"

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