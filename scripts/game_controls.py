import pyautogui
import threading

from properties import *

def mimic_press(input_key):
	# Mimic a press, add delay to detect and register
	pyautogui.keyDown(input_key)
	pyautogui.sleep(0.05)
	pyautogui.keyUp(input_key)

def game_input(input_key):
	threading.Thread(target=mimic_press, args=(input_key,)).start()

def start_combo():	
	mimic_press('f1')
	mimic_press(B_KEY)
	mimic_press(B_KEY)
	mimic_press(B_KEY)