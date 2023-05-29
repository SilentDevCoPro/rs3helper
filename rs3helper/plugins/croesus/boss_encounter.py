from rs3helper.utils.screen_capture import ScreenCapture
from rs3helper.utils.ocr import OCR
import re


class BossEncounter:
    def __init__(self, capture_area):
        self.capture_area = capture_area
        self.screen_capture = ScreenCapture()

    def detect_boss_encounter(self):
        """Detects the boss encounter by looking for a timer in the format "00:00"."""
        # Capture a screenshot of the predefined area
        cropped_screenshot = self.screen_capture.get_cropped_screenshot(self.capture_area)

        # Use the OCR class to extract text from the screenshot
        text = OCR.extract_text(cropped_screenshot)

        # Look for a time in the format "00:00"
        match = re.search(r"\b\d{2}:\d{2}\b", text)

        return match is not None  # Return True if a timer was found, False otherwise
