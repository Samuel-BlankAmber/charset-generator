from typing import Generator

from . import gen_charset
import keyboard


class KeyboardInterruptHandler:
    """Handles keyboard interruptions via a specified key."""

    def __init__(self):
        """
        Initialize the handler with default interrupt key 'esc' and set up the key press listener.
        """
        self.interrupt_key = "esc"
        self.interrupt_pressed = False
        keyboard.on_press(self._on_key_press)

    def _on_key_press(self, event):
        """
        Handle a keyboard event. If the pressed key matches the interrupt key,
        set the interrupt flag to True.

        Args:
            event: Keyboard event containing key information.
        """
        if event.name == self.interrupt_key:
            self.interrupt_pressed = True

    def set_interrupt_key(self, key: str):
        """
        Update the interrupt key and reset the interrupt flag.

        Args:
            key (str): New key to use for interruptions.
        """
        self.interrupt_key = key
        self.interrupt_pressed = False

    def reset(self):
        """
        Reset the interrupt flag to False.
        """
        self.interrupt_pressed = False


keyboard_handler = KeyboardInterruptHandler()


def yield_charset(regex: str, frequency_sorted: bool = False, allow_interruptions: bool = False, interrupt_key: str = "esc") -> Generator[str, None, None]:
    """
    Yield characters matching a regex, optionally allowing interruptions.

    Args:
        regex (str): Regular expression for character matching.
        frequency_sorted (bool): Use frequency-sorted characters if True.
        allow_interruptions (bool): If True, allow user input interruptions.
        interrupt_key (str): Key to trigger interruptions.

    Yields:
        str: Characters from the matched set or user input if interrupted.
    """
    if allow_interruptions:
        keyboard_handler.set_interrupt_key(interrupt_key)
    charset = gen_charset(regex, frequency_sorted)

    for char in charset:
        while allow_interruptions and keyboard_handler.interrupt_pressed:
            keyboard_handler.reset()
            while len(chosen_char := input("Enter a character: ")) != 1:
                print("Please enter a single character")
            yield chosen_char
        yield char
