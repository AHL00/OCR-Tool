# OCR-Tool
It is a image ocr tool made in Python using the Tesseract-OCR engine with the pytesseract package and has a GUI. This is my second ever python project so feel free to make any suggestions

# Release
- To install it, extract the zip that you downloaded. Put it in a folder like program files. There is a file called OCR-Tool.exe. You could make a shortcut and put it on your desktop for easy access. 
- Windows might say it's dangerous to run and block it. Just click "more info" and there you can run it. 
- If you download the version without tesseract included please check the dependencies section for instructions on how to add it. 

## Version 1.2
### With tesseract
https://drive.google.com/file/d/1EMS8cKsasorLRXpqVjLxo41nsAEk4SiF/view?usp=sharing
### Without tesseract
https://drive.google.com/file/d/1O4EYF9EmawT0VRSM6U1XkDBndGQBxDRe/view?usp=sharing
#### Changelog
- Fixed copy text button


# Features
- Modern GUI
- Snipping tool (Credit to harupy's python snipping tool)
- Open image from folder 
- Paste image from clipboard
- Save text to .txt
- Copy text to clipboard
- Cancel snip

# Dependencies
- Tesseract OCR Engine (UB Mannheim). Install either version 4 or 5. 5 is recommended as it performs better. Look for the installlation folder, the default is program files. Copy it into the same folder as main.py and rename the folder to "tesseract"
- Pytesseract
- PyQt5

# Known bugs
- White text doesnt work well

# Future features
- Better preprocessing to help with weird backgrounds
- Document ocr
- Menu
