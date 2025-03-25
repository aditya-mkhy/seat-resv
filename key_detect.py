from pynput import keyboard

class KeyPress:
    def __init__(self, key: keyboard.Key):
        self.key = key

    def wait(self):
        # Start listening for the key press
        with keyboard.Listener(on_press = self.on_press) as listener:
            listener.join()

        return True

    def on_press(self, key):
        if key == self.key:  # Wait for ESC key
            print(f"{self.key} is pressed..")
            return False  # Stop the listener


if __name__ == "__main__":
    key = keyboard.Key.shift_r
    KeyPress(key)
