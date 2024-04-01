import pygetwindow as gw
import pyautogui
import sys
import cv2

from properties import load
from game_controls import game_input
from properties import *

def init(roi_validate=True):
	global GAME_WINDOW

	load()
	
	# Open DeSmuME
	window_title = [title for title in gw.getAllTitles() if EMULATOR in title][0]
	window = gw.getWindowsWithTitle(window_title)[0]
	window.activate()
	window = gw.getActiveWindow()

	GAME_WINDOW["x_pos"] = GAME_WINDOW_OFFSET["x_offset"] + window.left
	GAME_WINDOW["y_pos"] = GAME_WINDOW_OFFSET["y_offset"] + window.top

	# Validate if entering and leaving roi are correct
	if roi_validate:
		cv2.imshow("Entering Luigi", "assets/luigi.png")
		cv2.imshow("Entering Baby Luigi", "assets/baby_luigi.png")
		cv2.imshow("Leaving", "assets/empty.png")
		cv2.waitKey(0)

		if pyautogui.confirm(text="Proceed?", title="Roi Validation Check", buttons=("Yes", "No")) != "Yes":
			cv2.destroyAllWindows() 
			sys.exit("Validation failed")

if __name__ == "__main__":
	pass