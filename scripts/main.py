import pygetwindow as gw
import pyautogui
import sys
import cv2
import numpy as np

from properties import load
from game_controls import start_combo, game_input
from game_states import update_states
from fixed_queue import FixedQueue
from properties import *

def get_frame():
	bbox = GAME_WINDOW["x_pos"], GAME_WINDOW["y_pos"], GAME_WINDOW["width"], GAME_WINDOW["height"]
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

	# Validate cv boxes if entering and leaving roi are correct
	if roi_validate:
		validate1 = cv2.imread("assets/baby_mario.png")
		validate2 = cv2.imread("assets/mario.png")

		cv2.rectangle(validate1, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
		cv2.rectangle(validate1, (LEAVING_ROI["x_pos"], LEAVING_ROI["y_pos"]), (LEAVING_ROI["x_pos"]+LEAVING_ROI["width"], LEAVING_ROI["y_pos"]+LEAVING_ROI["height"]), (255, 0, 0), 2)
		cv2.rectangle(validate2, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
		cv2.rectangle(validate2, (LEAVING_ROI["x_pos"], LEAVING_ROI["y_pos"]), (LEAVING_ROI["x_pos"]+LEAVING_ROI["width"], LEAVING_ROI["y_pos"]+LEAVING_ROI["height"]), (255, 0, 0), 2)

		cv2.imshow("Validation 1", validate1)
		cv2.imshow("Validation 2", validate2)

		# Prompt the user for confirmation
		if pyautogui.confirm(text="Proceed?", title="Roi Validation Check", buttons=("Yes", "No")) != "Yes":
			cv2.destroyAllWindows() 
			sys.exit("Validation failed")

		cv2.destroyAllWindows() 

def run_copy_flower():
	pass

def eval_genomes():
	pass

def run_neat():
	pass

def exit():
	pass

if __name__ == "__main__":
	init()
	run_neat()