import cv2
import numpy as np

from character import Character
from properties import *

# A small background frame, any pixel difference means a change in state
EDGE_WIDTH = 1
EDGE_BACKDROP = 0

# Character entering/leaving states
ENTERED_EDGE_STATE = False
LEAVING_STATE = False

# Predefined BGR color thresholds
LOWER_RED = np.array([0, 100, 100])
UPPER_RED = np.array([10, 255, 255])
LOWER_GREEN = np.array([50, 100, 100])
UPPER_GREEN = np.array([70, 255, 255])

def set_roi_backdrop(frame):
	global EDGE_BACKDROP

	roi = frame[ENTERING_ROI["y_pos"]:ENTERING_ROI["y_pos"]+ENTERING_ROI["height"],
			 ENTERING_ROI["x_pos"]:ENTERING_ROI["x_pos"]+EDGE_WIDTH]
	
	EDGE_BACKDROP = roi

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

def update_entering_state(character_queue, character_roi):
	global ENTERED_EDGE_STATE

	edge_roi = character_roi[:, :EDGE_WIDTH]

	if not np.array_equal(EDGE_BACKDROP, edge_roi) and False == ENTERED_EDGE_STATE: 
		ENTERED_EDGE_STATE = True

	elif np.array_equal(EDGE_BACKDROP, edge_roi) and True == ENTERED_EDGE_STATE:
		ENTERED_EDGE_STATE = False
		detected_character = detect_character(character_roi)
		character_queue.push(item=detected_character, priority=1)

	return character_queue

def update_leaving_state(character_queue, frame):
	global LEAVING_STATE

	leaving_roi = get_leaving_character_roi(frame)
	mask, _ = filter_mario_luigi(leaving_roi)
	leaving_roi = cv2.bitwise_and(leaving_roi, leaving_roi, mask=mask)

	# Acts like a debounce
	if np.any(leaving_roi) and False == LEAVING_STATE:
		LEAVING_STATE = True
		character_queue.pop()

	else: LEAVING_STATE = False
	
	return character_queue

def check_failure_state(frame):
	# TODO....

def update_states(frame, character_queue):
	character_roi = get_entering_character_roi(frame)
	character_queue = update_entering_state(character_roi)
	character_queue = update_leaving_state(frame)

	return character_queue

# load()

# thin_width = 1

# image = cv2.imread('assets/luigi.png')
# cv2.rectangle(image, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
# cv2.rectangle(image, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+thin_width, ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (255, 0, 0), 2)
# cv2.rectangle(image, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+35), (255, 0, 0), 2)

# image = get_entering_character_roi(image)
# print(detect_character(image))

# cv2.imshow("Image", image)
# cv2.waitKey(0)  # Wait for any key press
# cv2.destroyAllWindows()  # Close all OpenCV windows

# # 0.09813333333333334 0.0224