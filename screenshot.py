import os
import pygetwindow as gw
import pyautogui
import time
import numpy as np

from character import detect_character
from game_controls import start_combo

from queue import Queue
from collections import Counter

character_queue = Queue()
character_cache = []

# Function to capture the game window and save the screenshot
def capture_and_save_screenshot(folder_path, filename):
	# Create the folder if it doesn't exist
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

	# Get the game window
	game_window = gw.getActiveWindow()

	# Get the position and size of the game window
	x, y, width, height = game_window.left, game_window.top, game_window.width, game_window.height

	# Capture the screen within the game window region
	screenshot = pyautogui.screenshot(region=(x, y, width, height))

	# Save the screenshot
	screenshot.save(os.path.join(folder_path, filename))

	character = detect_character(np.array(screenshot)[:, :, ::-1])

	if character:
		character_cache.append(character)

	elif not character and character_cache:
		frequencies = Counter(character_cache)
		front_character = max(frequencies, key=frequencies.get)
		character_queue.put(front_character)
		character_cache.clear()

	

	# return detect_character(np.array(screenshot)[:, :, ::-1])


# Example usage
folder_path = "game_screenshots"
folder_increment = 1

start_combo()
# with open('log.txt', 'w') as file:
while (1):
	filename = f"screenshot_{folder_increment}.png"
	result = capture_and_save_screenshot(folder_path, filename)
	# file.write(f"{result}\n")
	folder_increment += 1
	time.sleep(1/100)

	print(list(character_queue.queue))
		

# import cv2
# image = cv2.imread('game_screenshots\screenshot_106.png')
# print(detect_character(image))