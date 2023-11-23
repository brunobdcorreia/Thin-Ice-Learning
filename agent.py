import subprocess
import time
import pydirectinput

def run_thin_ice():
    # Change the path to ThinIce.py accordingly
    thin_ice_path = "C:\\Users\\oknotok\\Documents\\computacao\\Thin-Ice-Python\\ThinIce.py"

    # Run Thin Ice game
    subprocess.Popen(["python", thin_ice_path])
    time.sleep(2)  # Wait for the game to start (adjust if needed)

def press_return():
    pydirectinput.press("return")

if __name__ == "__main__":
    run_thin_ice()
    
    # Simulate pressing the return key twice to start the game
    press_return()
    time.sleep(1)  # Adjust this delay if needed
    press_return()

    # Try to press the left arrow key
    while True:
        pydirectinput.press("left")
