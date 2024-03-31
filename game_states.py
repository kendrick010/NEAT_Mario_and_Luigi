import cv2
import numpy as np
from collections import Counter
from character import Character

CHARACTER_ROI_X = 5
CHARACTER_ROI_Y = 640
CHARACTER_ROI_WIDTH = 50
CHARACTER_ROI_HEIGHT = 75

LEAVING_ROI_X_OFFSET = 80
LEAVING_ROI_Y_OFFSET = 395
LEAVING_ROI_WIDTH = 75
LEAVING_ROI_HEIGHT = 25

CHARACTER_CACHE = []
LEAVING_MEM = False

# Create background subtractor object
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Predefined color thresholds
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
lower_blue = np.array([100, 100, 0])
upper_blue = np.array([255, 255, 10])

def get_character_roi(frame):
	'''
	Region of interest (ROI) enough to fit character sprites
	'''
	roi = frame[CHARACTER_ROI_Y:CHARACTER_ROI_Y+CHARACTER_ROI_HEIGHT, CHARACTER_ROI_X:CHARACTER_ROI_X+CHARACTER_ROI_WIDTH]

	return roi

def get_leaving_roi(frame):
	'''
	Region of interest (ROI) to detect characters leaving out of screen
	'''
	roi_x, roi_y = frame.shape[1] - LEAVING_ROI_X_OFFSET, frame.shape[0] - LEAVING_ROI_Y_OFFSET

	roi = frame[roi_y:roi_y+LEAVING_ROI_HEIGHT, roi_x:roi_x+LEAVING_ROI_WIDTH]

	return roi

def is_baby(roi, crop_depth=40, percent_threshold=0.90):
	'''
	Check if character sprite is a baby
	'''
	crop_hat = roi[:crop_depth, :]
	black_pixels = np.count_nonzero(np.all(crop_hat == [0, 0, 0], axis=-1))

	# Return baby if the cropped half does not show a hat
	percentage_baby = black_pixels / (crop_hat.shape[0] * crop_hat.shape[1])

	return True if percentage_baby > percent_threshold else False

def filter_mario_luigi(roi):
	'''
	Check if character sprite is mario
	'''
	hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

	mask_red = cv2.inRange(hsv, lower_red, upper_red)
	mask_green = cv2.inRange(hsv, lower_green, upper_green)

	return mask_red, mask_green

def filter_blues(roi):
	'''
	Track character contour by their blue pixels
	'''
	roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(roi_hsv, lower_blue, upper_blue)
	roi = cv2.bitwise_and(roi, roi, mask=mask)

	return roi

def detect_character(frame, red_percent_threshold=0.12, green_percent_threshold=0.05):
	'''
	Check what character enters the edge of screen
	'''
	roi = get_character_roi(frame)

	mask_red, mask_green = filter_mario_luigi(roi)

	# Calculate proportion of red and green
	red_pixels = cv2.countNonZero(mask_red) / (CHARACTER_ROI_WIDTH * CHARACTER_ROI_HEIGHT)
	green_pixels = cv2.countNonZero(mask_green) / (CHARACTER_ROI_WIDTH * CHARACTER_ROI_HEIGHT)

	# Classify what character is detected
	if red_percent_threshold > red_pixels and green_percent_threshold > green_pixels: return None

	# Check for baby case
	dominant_mask_color = mask_red if red_pixels > green_pixels else mask_green
	baby_sprite = is_baby(cv2.bitwise_and(roi, roi, mask=dominant_mask_color))

	if red_pixels > green_pixels and baby_sprite:
		return Character.BABY_MARIO
	
	elif red_pixels > green_pixels:
		return Character.MARIO
	
	elif green_pixels > red_pixels and baby_sprite:
		return Character.BABY_LUIGI
	
	else:
		return Character.LUIGI
	
def detect_leaving_character(frame):
	'''
	Check if any character is leaving off screen or changes in pixels
	'''
	mask, _ = filter_mario_luigi(frame)
	roi = cv2.bitwise_and(frame, frame, mask=mask)
	roi = get_leaving_roi(roi)

	# Acts like a debounce
	if np.any(roi) and False == LEAVING_MEM:
		return True

	return False

def display_change(frame, character_entering=False, character_leaving=False):
	if character_entering:
		cv2.rectangle(frame, (CHARACTER_ROI_X, CHARACTER_ROI_Y), (CHARACTER_ROI_X + CHARACTER_ROI_WIDTH, CHARACTER_ROI_Y + CHARACTER_ROI_HEIGHT), (0, 255, 0), 2)

	if character_leaving:
		leaving_x, leaving_y = frame.shape[1] - LEAVING_ROI_X_OFFSET, frame.shape[0] - LEAVING_ROI_Y_OFFSET
		cv2.rectangle(frame, (leaving_x, leaving_y), (leaving_x+LEAVING_ROI_WIDTH, leaving_y+LEAVING_ROI_HEIGHT), (0, 255, 0), 2)

	return frame

def update_queue(frame, character_queue):
	'''
	Check for entering and leaving characters, update the queue state
	'''
	global CHARACTER_CACHE, LEAVING_MEM
	
	# Update entering characters
	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	character = detect_character(frame_rgb)

	if character:
		CHARACTER_CACHE.append(character)

	elif CHARACTER_CACHE and None == character:
		frequencies = Counter(CHARACTER_CACHE)
		front_character = max(frequencies, key=frequencies.get)

		character_queue.put(front_character)
		CHARACTER_CACHE.clear()

	# Update leaving characters
	if detect_leaving_character(frame): 
		character_queue.get()
		LEAVING_MEM = True

	LEAVING_MEM = False

	return character_queue

def get_sprite_contour_pos(contour):
	'''
	Get center pixel coordinate of sprite contour
	'''
	contour_x, contour_y, contour_w, contour_h = cv2.boundingRect(contour)

	center_x_offset, center_y_offset = int(contour_w/2), int(contour_h/2)

	return (contour_x + center_x_offset, contour_y + center_y_offset)	

def get_sprites_contours(frame, min_contour_size=70, max_contour_size=300):
	'''
	Get all moving sprite contours on screen and return their positions
	'''
	frame_hsv = filter_blues(frame)

	frame_gray = cv2.cvtColor(frame_hsv, cv2.COLOR_BGR2GRAY)
	fg_mask = bg_subtractor.apply(frame_gray)

	# Threshold the foreground mask and find contours
	_, thresh = cv2.threshold(fg_mask, 240, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = [get_sprite_contour_pos(cnt) for cnt in contours if max_contour_size > cv2.contourArea(cnt) > min_contour_size]

	return contours

def update_states(frame, character_queue, display=False):
	'''
	Update universal game state including characters in screen and potential sprite positions
	'''
	character_queue = update_queue(frame, character_queue)
	character_positions = get_sprites_contours(frame)

	if display:
		overlay = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		cv2.imshow('Change of States', overlay)

	return character_queue, character_positions
