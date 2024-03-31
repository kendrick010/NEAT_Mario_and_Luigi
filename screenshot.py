import pygetwindow as gw
import pyautogui
import time
import numpy as np
import cv2

from game_states import update_states
from game_controls import start_combo

from queue import Queue

# Function to capture the game window
def capture_and_save_screenshot(character_queue):
	# Get the game window
	frame = pyautogui.screenshot(region=bbox)
	frame = np.array(frame)

	return update_states(frame, character_queue, display=True)


start_combo()
character_queue = Queue()
character_pos = []
game_window = gw.getActiveWindow()
bbox = game_window.left, game_window.top, game_window.width, game_window.height

while (1):
	character_queue, character_pos = capture_and_save_screenshot(character_queue)
	time.sleep(1/100)

	# Break the loop if 'q' is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release resources
cv2.destroyAllWindows()

# import cv2
# image = cv2.imread('game_screenshots\screenshot_106.png')
# print(detect_character(image))