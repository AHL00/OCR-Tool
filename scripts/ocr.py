#Packagesv
from PIL import Image, ImageEnhance, ImageGrab
import pytesseract
import os.path

#Location of Tesseract OCR
if os.path.exists("tesseract/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"tesseract\tesseract"

#Functions
def preprocess_image(image):
    imageGrayscale = image.convert('L')
    imageGrayscaleContrast = ImageEnhance.Contrast(imageGrayscale)
    imageGrayscaleContrast = imageGrayscaleContrast.enhance(2)
    return imageGrayscaleContrast

def image_ocr(imagePath):
    data = pytesseract.image_to_string(preprocess_image(Image.open(imagePath)))
    return data

def image_ocr_clipboard():
    if(ImageGrab.grabclipboard()):
        data = pytesseract.image_to_string(preprocess_image(ImageGrab.grabclipboard()))
    else:
        data = None
    return data