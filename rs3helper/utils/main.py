from rs3helper.utils.screen_capture import ScreenCapture
from rs3helper.utils.ocr import OCR
from pynput.mouse import Listener
import matplotlib.pyplot as plt

clicks = []


def on_click(x, y, button, pressed):
    if pressed:
        clicks.append((x, y))
        print('Mouse clicked at ({0}, {1})'.format(x, y))
        if len(clicks) == 2:
            # Stop listener
            clicks.sort()
            return False


def main():
    # Create a ScreenCapture object
    screen_capture = ScreenCapture()

    cropped_screenshot = screen_capture.get_cropped_screenshot(clicks)

    # Use the OCR class to extract text from the screenshot
    text = OCR.extract_text(cropped_screenshot)

    # Print the extracted text
    print(text)

    plt.imshow(cropped_screenshot)
    plt.show()


if __name__ == "__main__":
    with Listener(on_click=on_click) as listener:
        listener.join()

    main()
    # Collect events until released
