import json

EMULATOR = "DeSmuME"

GAME_WINDOW = {"x_pos": 0, "y_pos": 0, "width": 0, "height": 0}
GAME_WINDOW_OFFSET = {"x_offset": 0, "y_offset": 0}

ENTERING_ROI = {"x_pos": 0, "y_pos": 0, "width": 0, "height": 0}
LEAVING_ROI = {"x_pos": 0, "y_pos": 0, "width": 0, "height": 0}
LEAVING_FREQ = 0

RESET_KEY = "f3"
UP_KEY = "up"
DOWN_KEY = "down"
RIGHT_KEY = "right"
LEFT_KEY = "left"
A_KEY = "D"
B_KEY = "S"
X_KEY = "W"
Y_KEY = "A"

RECORD_VIDEO = False

def load(filename="properties.json"):    
    global GAME_WINDOW, ENTERING_ROI, LEAVING_ROI, RECORD_VIDEO
    global UP_KEY, DOWN_KEY, RIGHT_KEY, LEFT_KEY
    global A_KEY, B_KEY, X_KEY, Y_KEY
    global LEAVING_FREQ, RECORD_VIDEO
    
    # I know it's messy
    with open(filename, "r") as property_file:
        attributes = json.load(property_file)

        GAME_WINDOW_OFFSET["x_offset"] = attributes["gameScreenOffsetX"]
        GAME_WINDOW_OFFSET["y_offset"] = attributes["gameScreenOffsetY"]
        GAME_WINDOW["width"] = attributes["gameScreenWidth"]
        GAME_WINDOW["height"] = attributes["gameScreenHeight"]

        ENTERING_ROI["x_pos"] = attributes["characterRoiX"]
        ENTERING_ROI["y_pos"] = attributes["characterRoiY"]
        ENTERING_ROI["width"] = attributes["characterRoiWidth"]
        ENTERING_ROI["height"] = attributes["characterRoiHeight"]

        LEAVING_ROI["x_pos"] = attributes["leavingRoiX"]
        LEAVING_ROI["y_pos"] = attributes["leavingRoiY"]
        LEAVING_ROI["width"] = attributes["leavingRoiWidth"]
        LEAVING_ROI["height"] = attributes["leavingRoiHeight"]

        LEAVING_FREQ = attributes["leavingLambdaFreq"]

        UP_KEY = attributes["upKey"]
        DOWN_KEY = attributes["downKey"]
        RIGHT_KEY = attributes["rightKey"]
        LEFT_KEY = attributes["leftKey"]

        A_KEY = attributes["aKey"]
        B_KEY = attributes["bKey"]
        X_KEY = attributes["xKey"]
        Y_KEY = attributes["yKey"]

        RECORD_VIDEO = attributes["recordVideo"]