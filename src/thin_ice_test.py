import os
import subprocess
import pyautogui
import time

# Define the path to the ThinIce.py file
thin_ice_path = "C:\\Users\\oknotok\\Documents\\computacao\\Thin-Ice-Python\\ThinIce.py"

# Open the ThinIce.py file
subprocess.Popen(["py", thin_ice_path])

# # Wait for the game to start
# time.sleep(2)

# # Send keyboard and mouse inputs to play the game
# # Example: move the mouse to position (x, y) and click
# pyautogui.moveTo(x, y)
# pyautogui.click()

# # Example: press a key
# pyautogui.press('space')

# # Example: press a key with a duration
# pyautogui.keyDown('left')
# time.sleep(1)
# pyautogui.keyUp('left')

# # Close the game
# os.system("taskkill /f /im python.exe")
