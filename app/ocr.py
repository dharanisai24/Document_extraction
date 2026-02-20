import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_document(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        pages = convert_from_path(
            file_path,
            poppler_path=r"C:\Users\dhara\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
        )

        for page in pages:
            text += pytesseract.image_to_string(page)

    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text