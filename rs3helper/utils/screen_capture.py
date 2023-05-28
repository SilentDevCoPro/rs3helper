from PIL import Image
from mss import mss
import numpy as np
from typing import List, Tuple


class ScreenCapture:
    """
    A class used to capture and manipulate screenshots.

    ...

    Attributes
    ----------
    sct : mss.mss
        an MSS object used to capture screenshots
    monitor : dict
        the monitor to capture screenshots from

    Methods
    -------
    _capture():
        Captures a screenshot and returns it as a NumPy array.
    _get_screen_offset():
        Calculates the screen offset.
    get_cropped_screenshot(clicks):
        Returns a cropped screenshot based on provided click coordinates.
    """

    def __init__(self):
        """
        Initializes the ScreenCapture with an MSS object and the second monitor.
        """
        self.sct = mss()
        self.monitor = self.sct.monitors[2]

    def _capture(self) -> np.ndarray:
        """
        Captures a screenshot from the defined monitor.

        Returns
        -------
        np.ndarray
            The screenshot as a NumPy array.
        """
        screenshot = self.sct.grab(self.monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return np.array(img)

    def _get_screen_offset(self) -> Tuple[int, int]:
        """
        Calculates the screen offset by comparing the width and height of the monitor to its right and bottom edges.

        Returns
        -------
        Tuple[int, int]
            The x and y offsets of the screen.
        """
        offset_x = (self.monitor["width"] - self.monitor["right"]) // 2
        offset_y = (self.monitor["height"] - self.monitor["bottom"]) // 2

        return offset_x, offset_y

    def get_cropped_screenshot(self, clicks: List[Tuple[int, int]]) -> np.ndarray:
        """
        Returns a cropped screenshot based on provided click coordinates.

        Parameters
        ----------
        clicks : List[Tuple[int, int]]
            A list of tuples, where each tuple contains the x and y coordinates of a click.

        Returns
        -------
        np.ndarray
            The cropped screenshot as a NumPy array.
        """
        screenshot = self._capture()

        # Adjust the mouse click coordinates
        clicks_adjusted = [(x - self.monitor["left"], y - self.monitor["top"]) for x, y in clicks]

        roi = (int(clicks_adjusted[0][0]), int(clicks_adjusted[0][1]),
               int(clicks_adjusted[1][0] - clicks_adjusted[0][0]), int(clicks_adjusted[1][1] - clicks_adjusted[0][1]))
        return screenshot[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
