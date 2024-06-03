from pynput import mouse, keyboard
import json
import time
import threading
import os

# List to store the coordinates
coordinates = []

# Flag to determine if the program should start saving coordinates
start_saving = False

# Flag to determine if the script should stop
stop_program = False

# Function to load existing coordinates from JSON file
def load_existing_coordinates(filename='coordinates.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

# Function to save coordinates continuously
def save_coordinates():
    global coordinates
    global stop_program
    while not stop_program:
        if start_saving:
            # Get current mouse position and add to the coordinates list
            coordinates.append(mouse.Controller().position)
            time.sleep(0.07)

# Function to handle key press events
def on_press(key):
    global start_saving
    global stop_program
    if key == keyboard.KeyCode.from_char('s'):
        # Set the flag to start saving coordinates if 's' key is pressed
        start_saving = True
        print("Starting to save coordinates...")
        # Start a separate thread to continuously save coordinates
        threading.Thread(target=save_coordinates).start()
    elif key == keyboard.KeyCode.from_char('f'):
        # Set the flag to stop the program if 'f' key is pressed
        stop_program = True
        print("Stopping the program...")
        return False  # Stop the listener

# Load existing coordinates
coordinates = load_existing_coordinates()

# Start the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Wait until the stop_program flag is set to True
keyboard_listener.join()

# Save coordinates to a JSON file
with open('coordinates.json', 'w') as file:
    json.dump(coordinates, file)

print("Final list of coordinates saved to coordinates.json:", coordinates)