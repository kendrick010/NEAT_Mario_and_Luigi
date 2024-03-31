import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
from game_controls import start_combo

start_combo()
game_window = gw.getActiveWindow()

# Get the position and size of the game window
crop_top_screen = 460
crop_height = 300
bbox = game_window.left, game_window.top + crop_top_screen, game_window.width, crop_height

# Create background subtractor object
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

def detect_leave(frame, threshold=0.98):
    roi_x = game_window.width - 75  # Adjust as needed
    roi_y = 0  # Adjust as needed
    roi_width = 75  # Adjust as needed
    roi_height = 25  # Adjust as needed

    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    if np.any(roi):
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 255, 0), 2)
    
    return frame

def get_contours(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)
    frame = cv2.bitwise_and(frame, frame, mask=mask)

    frame = detect_leave(frame)
    cv2.imshow('Color filter', frame)
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply background subtraction
    fg_mask = bg_subtractor.apply(gray)
    
    # Threshold the foreground mask
    _, thresh = cv2.threshold(fg_mask, 240, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on size
    min_contour_size = 70  # Adjust this value as needed
    max_contour_size = 300  # Adjust this value as needed
    filtered_contours = [cnt for cnt in contours if max_contour_size > cv2.contourArea(cnt) > min_contour_size]

    return filtered_contours

while True:
    # Capture frame from the specific window
    frame = np.array(pyautogui.screenshot(region=bbox))

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    # lower_green = np.array([50, 100, 100])
    # upper_green = np.array([70, 255, 255])

    filtered_contours = []
    filtered_contours += get_contours(frame, lower_red, upper_red)
    # filtered_contours += get_contours(frame, lower_green, upper_green)
    
    # Draw rectangles around moving objects
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Convert BGR to RGB for displaying
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Display the frame
    cv2.imshow('Motion Detection', frame_rgb)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()