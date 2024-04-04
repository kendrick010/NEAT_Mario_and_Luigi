import pyautogui
import threading

from properties import *

PRESS_STATE = False
READING = True
INPUT_KEY = None

def mimic_press(input_key):
	# Mimic a press, add delay to detect and register
	pyautogui.keyDown(input_key)
	pyautogui.sleep(0.05)
	pyautogui.keyUp(input_key)

def game_input_listener():
	global PRESS_STATE
	
	while True:
		if PRESS_STATE and not READING:
			mimic_press(INPUT_KEY)
			PRESS_STATE = False

def game_input(input_key):
	global PRESS_STATE, INPUT_KEY

	PRESS_STATE = True
	INPUT_KEY = input_key

def start_combo():	
	global READING

	READING = False

	mimic_press('f1')
	mimic_press(B_KEY)
	mimic_press(B_KEY)
	mimic_press(B_KEY)

event_thread = threading.Thread(target=game_input_listener)
event_thread.start()