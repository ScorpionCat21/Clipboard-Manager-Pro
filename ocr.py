import pytesseract
from PIL import Image
import io

def image_to_text(img_data):
    try:
        image = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return ""