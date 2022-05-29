# TODO
# Adjust text size to 32 px
# Crop image before rotation
# Fix rotation

# Order of image processing
# -------------------------
# </> Contrast
# </> Black and White colors
# </> Threshold 
# </> Black background
# </> Crop before rotating
# < > Rotate text

#Packages
from PIL import Image, ImageEnhance, ImageGrab
import cv2
import numpy as np
import pytesseract
import os.path

#Location of Tesseract OCR
if os.path.exists("tesseract/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"tesseract\tesseract"

#Functions
def preprocess_image(im):
    pilImage = im.convert('RGB') 

    #Contrast
    contrast = ImageEnhance.Contrast(pilImage).enhance(10)

    #Convert to cv2 image
    contrast = cv2.cvtColor(np.array(contrast), cv2.COLOR_BGRA2RGBA)

    #Black and White
    bw = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

    #Thresholding
    thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]
    
    #Black background
    avgColorPerRow = np.average(thresh, axis=0) 
    avgColor = np.average(avgColorPerRow, axis=0)
    global blackbg
    if avgColor > 127.5:
        blackbg = cv2.bitwise_not(thresh)
        blackbg 
    else: 
        blackbg = thresh

    #Crop
    coords = np.column_stack(np.where(blackbg > 0))
    (textW, textH) = cv2.minAreaRect(coords)[1][:2]
    cropSize = int(max(textW, textH))
    padded = cv2.copyMakeBorder(blackbg, int(cropSize/2), int(cropSize/2), int(cropSize/2), int(cropSize/2), cv2.BORDER_CONSTANT, None, value = 0)
    
    #Rotate
    coords = np.column_stack(np.where(padded > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < 45:
        angle = -(90 + angle)
    else:
        angle = -angle
    angle = 0
    (h, w) = padded.shape[:2]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(padded, m, (w, h),
    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    cv2.imshow('image', rotated)

    # Add resizeing image, intelligent color change
    return rotated

def image_ocr(imagePath):
    data = pytesseract.image_to_string(preprocess_image(Image.open(imagePath)))
    dict = {'text': data, 'image': Image.open(imagePath)}
    return dict

def image_ocr_pillow_image(image):
    data = pytesseract.image_to_string(preprocess_image(image))
    dict = {'text': data, 'image': image}
    return dict

def image_ocr_clipboard():
    if(ImageGrab.grabclipboard()):
        data = pytesseract.image_to_string(preprocess_image(ImageGrab.grabclipboard()))
    else:
        data = None
    dict = {'text': data, 'image': ImageGrab.grabclipboard()}
    return dict

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return data[s < m].tolist()