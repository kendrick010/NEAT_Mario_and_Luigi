from enum import Enum
import cv2
import numpy as np

ROI_WIDTH = 50
ROI_HEIGHT = 75

class Character(Enum):
    MARIO = 1
    LUIGI = 2
    BABY_MARIO = 3
    BABY_LUIGI = 4

def get_roi(image):
    '''
    Region of interest (ROI) enough to fit character sprites
    '''
    roi_x, roi_y = 5, 640

    roi = image[roi_y:roi_y+ROI_HEIGHT, roi_x:roi_x+ROI_WIDTH]

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

    # Create a mask to filter the red color in the image
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Create a mask to filter the green color in the image
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    return mask_red, mask_green

def detect_character(image, red_percent_threshold=0.12, green_percent_threshold=0.05):
    '''
    Check what character enters the edge of screen
    '''
    roi = get_roi(image)

    mask_red, mask_green = filter_mario_luigi(roi)

    # Calculate proportion of red and green
    red_pixels = cv2.countNonZero(mask_red) / (ROI_WIDTH * ROI_HEIGHT)
    green_pixels = cv2.countNonZero(mask_green) / (ROI_WIDTH * ROI_HEIGHT)

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



# image = cv2.imread('assets/luigi.png')
# print(detect_character(image))

# print(red_pixels)
# print(green_pixels)

# # Display the filtered red and green images
# cv2.imshow('Filtered Red Color', cv2.bitwise_and(roi, roi, mask=mask_red))
# cv2.imshow('Filtered Green Color', cv2.bitwise_and(roi, roi, mask=mask_green))
# cv2.waitKey(0)
# cv2.destroyAllWindows()