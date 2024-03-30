# screenshot_103 - luigi
# screenshot_81 - babyluigi
# screenshot_136 - mario
# screenshot_81 - babymario


# next pos  screenshot_142

import cv2

# Read an image
image = cv2.imread('game_screenshots\screenshot_136.png')

# Define the coordinates of the region of interest (ROI)
x, y, width, height = 5, 640, 50, 75  # Example coordinates (adjust as needed)

head_crop = 40

# Draw a rectangle around the ROI on the original image
cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Green rectangle, thickness = 2
cv2.rectangle(image, (x, y), (x + width, y + head_crop), (255, 0, 0), 2)  # Green rectangle, thickness = 2

# Crop the ROI from the image
roi = image[y:y+height, x:x+width]

# Display the image with the rectangle overlay
cv2.imshow('Image with ROI', image)
cv2.waitKey(0)
cv2.destroyAllWindows()