import pygetwindow as gw
import pyautogui
import sys
import cv2
import numpy as np

from properties import load
from game_controls import game_input, start_combo
from game_states import set_roi_backdrop
from priority_queue import FixedLengthPriorityQueue
from character import Character
from properties import *

def get_frame(bbox):
	frame = np.array(pyautogui.screenshot(region=bbox))
				  
	return frame

def init(roi_validate=True):
	global GAME_WINDOW, CHARACTER_QUEUE

	load()
	
	# Open DeSmuME
	window_title = [title for title in gw.getAllTitles() if EMULATOR in title][0]
	window = gw.getWindowsWithTitle(window_title)[0]
	window.activate()	
	pyautogui.sleep(1)
	window = gw.getActiveWindow()

	GAME_WINDOW["x_pos"] = GAME_WINDOW_OFFSET["x_offset"] + window.left
	GAME_WINDOW["y_pos"] = GAME_WINDOW_OFFSET["y_offset"] + window.top

	bbox = GAME_WINDOW["x_pos"], GAME_WINDOW["y_pos"], GAME_WINDOW["width"], GAME_WINDOW["height"]

	# Validate if entering and leaving roi are correct
	# if roi_validate:

	# 	cv2.imshow("Entering Luigi", cv2.cvtColor(np.array(pyautogui.screenshot(region=bbox)), cv2.COLOR_BGR2RGB))
	# 	cv2.waitKey(0)
	# 	# cv2.imshow("Entering Baby Luigi", "assets/baby_luigi.png")
	# 	# cv2.imshow("Leaving", "assets/empty.png")


	# 	# if pyautogui.confirm(text="Proceed?", title="Roi Validation Check", buttons=("Yes", "No")) != "Yes":
	# 	# 	cv2.destroyAllWindows() 
	# 	# 	sys.exit("Validation failed")

	# 	cv2.destroyAllWindows() 

	# A small background frame, to compare pixel difference amd check for state changes
	frame = get_frame(bbox)
	set_roi_backdrop(frame)

if __name__ == "__main__":
	init()

	# Max possibele number of marios and luigis can appear in one frame is about 3-4 on higher speeds
	CHARACTER_QUEUE = FixedLengthPriorityQueue(max_length=4)