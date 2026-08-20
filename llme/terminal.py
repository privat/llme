"""Terminal display primitives (no llme internal dependencies)."""

import itertools
import re
import sys
import threading
import time

from termcolor import colored, cprint


class ChunkPrinter:
    """Print chunks of text and gracefully handle scope change, newlines, and partial unicode"""

    def __init__(self):
        self.last = None
        self.id = None
        self.inside_string = False

    def print(self, s, color=None, on_color=None, id=None):
        """Print a colored text, no '\n', forced flush.
        If id is set, then a different id will force a newline."""
        if not s:
            return
        if id != self.id:
            self.end()
            self.id = id
        cprint(s, color, on_color, end="", flush=True)
        self.last = s

    def print_escaped(self, s, color=None, string_color=None, on_color=None, id=None):
        """Assume that s contains strings with escaped content. We un-escape and change the color"""
        items = re.split(r"(\\[n\"\\]|\")", s)
        for i in items:
            if not i:
                continue
            elif i == "\"":
                self.inside_string = not self.inside_string
                self.print(i, color, on_color, id=id)
            elif i == "\\n":
                self.print("\n", color, on_color, id=id)
            else:
                if i[0] == "\\":
                    i = i[1:]
                c = string_color if self.inside_string else color
                self.print(i, c, on_color, id=id)

    def end(self):
        """Add possible final newline"""
        if self.last and self.last[-1] != '\n':
            print("")
            self.last = None
        self.inside_string = False

class Spinner:
    """A simple context manager for a spinner animation.
    It gives the user a feedback on long computation or network request.

    :param color: color of the spinner with termcolor nomenclature.
    :param disabled: if True, Spinner do nothing. The default is `not sys.stdout.isatty()`. Use False to force the spin.
    :param sequence: string of characters to animate.
    :param speed: animation speed in Hz.

    Usage:
        with Spinner("blue"):
            do_something()
    """
    def __init__(self, color="white", disabled=None, sequence="⠋⠙⠹⠽⠼⠴⠦⠧⠇⠏", speed=10):
        self.color = color
        if disabled is None:
            disabled = not sys.stdout.isatty()
        self.disabled = disabled
        self.sequence = sequence
        self.speed = speed
        self.stop_event = None
        self.animation_thread = None

    def _animate(self):
        """Animation loop, run in a thread."""
        for c in itertools.cycle(self.sequence):
            if self.stop_event.is_set():
                break
            sys.stdout.write(f"\r{colored(c, self.color)} ")
            sys.stdout.flush()
            time.sleep(1/self.speed)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def stop(self):
        """Manually stop the spin."""
        if self.disabled:
            return
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.animation_thread.join()

    def __enter__(self):
        if not self.disabled:
            self.stop_event = threading.Event()
            self.animation_thread = threading.Thread(target=self._animate)
            self.animation_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()
