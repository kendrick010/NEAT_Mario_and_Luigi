import cv2
import numpy as np
from collections import Counter

from character import Character
from properties import *

# Character entering/leaving states
CHARACTER_CACHE = []
LAST_ENTERED = 0
LEAVING_STATE = False

# Predefined BGR color thresholds
LOWER_RED = np.array([0, 100, 100])
UPPER_RED = np.array([10, 255, 255])
LOWER_GREEN = np.array([50, 100, 100])
UPPER_GREEN = np.array([70, 255, 255])

def get_entering_character_roi(frame):
	roi = frame[ENTERING_ROI["y_pos"]:ENTERING_ROI["y_pos"]+ENTERING_ROI["height"],
			 ENTERING_ROI["x_pos"]:ENTERING_ROI["x_pos"]+ENTERING_ROI["width"]]
	
	return roi

def get_leaving_character_roi(frame):
	roi = frame[LEAVING_ROI["y_pos"]:LEAVING_ROI["y_pos"]+LEAVING_ROI["height"],
			 LEAVING_ROI["x_pos"]:LEAVING_ROI["x_pos"]+LEAVING_ROI["width"]]
	
	return roi

def is_baby(character_roi, crop_hat_depth=35, percent_threshold=0.90):
	crop_hat = character_roi[:crop_hat_depth, :]
	black_pixels = np.count_nonzero(np.all(crop_hat == [0, 0, 0], axis=-1))

	# Return baby if the cropped half does not show a hat
	percentage_baby = black_pixels / (crop_hat.shape[0] * crop_hat.shape[1])

	return True if percentage_baby > percent_threshold else False

def filter_mario_luigi(character_roi):
	hsv = cv2.cvtColor(character_roi, cv2.COLOR_BGR2HSV)

	mask_red = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
	mask_green = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

	return mask_red, mask_green

def detect_character(character_roi, red_percent_threshold=0.13, green_percent_threshold=0.08):
	mask_red, mask_green = filter_mario_luigi(character_roi)

	# Calculate proportion of red and green
	red_percent = cv2.countNonZero(mask_red) / (ENTERING_ROI["width"] * ENTERING_ROI["height"])
	green_percent = cv2.countNonZero(mask_green) / (ENTERING_ROI["width"] * ENTERING_ROI["height"])

	# Classify what character is detected
	if red_percent_threshold > red_percent and green_percent_threshold > green_percent: return Character.EMPTY

	# Check for baby case
	dominant_mask_color = mask_red if red_percent > green_percent else mask_green
	baby_sprite = is_baby(cv2.bitwise_and(character_roi, character_roi, mask=dominant_mask_color))

	if red_percent > green_percent and baby_sprite:
		return Character.BABY_MARIO
	
	elif red_percent > green_percent:
		return Character.MARIO
	
	elif green_percent > red_percent and baby_sprite:
		return Character.BABY_LUIGI
	
	else:
		return Character.LUIGI

def update_entering_state(character_roi, character_queue):
	global CHARACTER_CACHE

	character_roi = cv2.cvtColor(character_roi, cv2.COLOR_BGR2RGB)
	found_character = detect_character(character_roi)

	if Character.EMPTY != found_character:
		CHARACTER_CACHE.append(found_character)

	elif CHARACTER_CACHE and Character.EMPTY == found_character:
		frequencies = Counter(CHARACTER_CACHE)
		front_character = max(frequencies, key=frequencies.get)

		character_queue.push(front_character)
		CHARACTER_CACHE.clear()

	return character_queue

def update_leaving_state(leaving_roi, character_queue):
	global LEAVING_STATE

	mask, _ = filter_mario_luigi(leaving_roi)
	leaving_roi = cv2.bitwise_and(leaving_roi, leaving_roi, mask=mask)

	# Acts like a debounce
	if np.any(leaving_roi) and False == LEAVING_STATE:
		LEAVING_STATE = True
		character_queue.pop()

		print('left')

	elif not np.any(leaving_roi) and True == LEAVING_STATE: 
		LEAVING_STATE = False
	
	return character_queue

def check_failure_state(frame, percent_threshold=0.05):
	leaving_roi = get_leaving_character_roi(frame)
	hsv = cv2.cvtColor(leaving_roi, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
	menu_percent = cv2.countNonZero(mask) / (LEAVING_ROI["width"] * LEAVING_ROI["height"])

	if menu_percent > percent_threshold: return True

	return False

def update_states(frame, character_queue):
	character_roi = get_entering_character_roi(frame)
	character_queue = update_entering_state(character_roi, character_queue)

	leaving_roi = get_leaving_character_roi(frame)
	character_queue = update_leaving_state(leaving_roi, character_queue)

	return character_queue





# image = cv2.imread('assets/luigi.png')
# cv2.rectangle(image, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
# cv2.rectangle(image, (LEAVING_ROI["x_pos"], LEAVING_ROI["y_pos"]), (LEAVING_ROI["x_pos"]+LEAVING_ROI["width"], LEAVING_ROI["y_pos"]+LEAVING_ROI["height"]), (255, 0, 0), 2)

# image = get_entering_character_roi(image)
# from priority_queue import FixedLengthPriorityQueue
# CHARACTER_QUEUE = FixedLengthPriorityQueue(max_length=4)
# print(detect_character(image))

	# Open DeSmuME
# window_title = [title for title in gw.getAllTitles() if EMULATOR in title][0]
# window = gw.getWindowsWithTitle(window_title)[0]
# window.activate()	
# pyautogui.sleep(1)
# window = gw.getActiveWindow()

# GAME_WINDOW["x_pos"] = GAME_WINDOW_OFFSET["x_offset"] + window.left
# GAME_WINDOW["y_pos"] = GAME_WINDOW_OFFSET["y_offset"] + window.top

# frame = get_frame()
# print(check_failure_state(frame))

# cv2.imshow("Image", frame)
# cv2.waitKey(0)  # Wait for any key press
# cv2.destroyAllWindows()  # Close all OpenCV windows

# # 0.09813333333333334 0.0224