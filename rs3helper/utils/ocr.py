import pytesseract


class OCR:
    @staticmethod
    def extract_text(image):
        text = pytesseract.image_to_string(image)
        return text
