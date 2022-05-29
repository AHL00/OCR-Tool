
#packages
import clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QMessageBox, QFrame
import sys, os.path

#scripts
from scripts import ocr, screenshot



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OCR Tool")
        self.setWindowIcon(QIcon('icon.ico'))

        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.setFixedSize(250, 75)

        self.messageLabel = QLabel(wid)
        self.messageLabel.setText("OCR Tool")
        self.messageLabel.setFont(QFont('', 15))
        self.messageLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.messageLabel.setAlignment(Qt.AlignCenter)

        self.imageFileOcrButton = QPushButton(wid)
        self.imageFileOcrButton.setText("Open image")
        self.imageFileOcrButton.clicked.connect(self.ocr_image_file_button_press)

        self.imageCopyOcrButton = QPushButton(wid)
        self.imageCopyOcrButton.setText("Paste Image")
        self.imageCopyOcrButton.clicked.connect(self.ocr_image_paste_button_press)

        self.imageSSOcrButton = QPushButton(wid)
        self.imageSSOcrButton.setText("Screenshot")
        self.imageSSOcrButton.clicked.connect(lambda: (ss.start(window), self.hide()))

        layoutV = QVBoxLayout()
        layoutButton = QHBoxLayout()
        layoutMessage = QHBoxLayout()

        layoutMessage.addWidget(self.messageLabel)

        layoutButton.addWidget(self.imageFileOcrButton)
        layoutButton.addWidget(self.imageCopyOcrButton)
        layoutButton.addWidget(self.imageSSOcrButton)

        layoutV.addLayout(layoutMessage)
        layoutV.addLayout(layoutButton)
        wid.setLayout(layoutV)

    def ocr_image_file_button_press(self):
        filePath = self.open_image_file_dialog()
        if filePath:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            data = ocr.image_ocr(filePath)
            self.outputWindow = OutputWindow(data['text'], os.path.basename(filePath), data['image'])
            self.outputWindow.show()
            QApplication.restoreOverrideCursor()
    
    def ocr_image_paste_button_press(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)        
        data = ocr.image_ocr_clipboard()
        if(data['image']):
            outputWindow = OutputWindow(data['text'], "Copied image", data['image'])
            outputWindow.show()
        else:
            QApplication.restoreOverrideCursor()
            errorMessage = ErrorMsg(message="No image in clipboard")
            errorMessage.show()
        QApplication.restoreOverrideCursor()

    def screenshot_done(self, img):
        self.show()
        QApplication.setOverrideCursor(Qt.WaitCursor)  
        data = ocr.image_ocr_pillow_image(img)
        self.outputWindow = OutputWindow(data['text'], "Screenshot", data['image'])
        self.outputWindow.show()
        QApplication.restoreOverrideCursor()

    def open_image_file_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Open Image", "","Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            return fileName



class ErrorMsg(QMessageBox):
    def __init__(self, message):
        super(ErrorMsg, self).__init__()
        self.message = message   
        self.setWindowIcon(QIcon('icon.ico'))
        self.setIcon(QMessageBox.Warning)
        self.setText(self.message)
        self.setWindowTitle("Error")
        self.exec_()



class OutputWindow(QDialog):
    def __init__(self, text, fileName, image):
        super().__init__()
        self.init_output_window(text, fileName, image)

    '''def resizeEvent(self, event):
        #coeff = self.pixmap.width / self.width
        #print(self.pixmap.width)
        #self.width
        newHeight = self.width() / self.imageAspectRatio[0]
        self.pixmap = self.pixmap.scaled(self.width(), newHeight)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.resize(self.width(), newHeight)'''

    def init_output_window(self, text, fileName, image):
        self.text = text
        self.fileName = fileName
        #self.image = image
        self.setWindowTitle(text[0:24] + '...')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setMinimumSize(150, 100)
        
        '''self.imageSize = [self.image.size[0], self.image.size[1]]     
        self.imageAspectRatio = [self.imageSize[0] / self.imageSize[1] , 1]

        self.image = self.image.convert("RGBA")
        self.image = self.image.tobytes("raw","RGBA")
        self.image = QImage(self.image, self.imageSize[0], self.imageSize[1], QImage.Format_RGBA8888)

        self.pixmap = QPixmap().fromImage(self.image)
        #self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.pixmap)
        #self.imageLabel.setScaledContents(True)
        '''

        self.scrollableLabel = ScrollLabel()
        self.scrollableLabel.setText(self.text)
        self.scrollableLabel.setMinimumSize(0, 50)

        self.copyButton = QPushButton()
        self.copyButton.setText("Copy text")
        self.copyButton.clicked.connect(lambda: self.copy_button_click(text))
        self.copyButton.setFocusPolicy(Qt.NoFocus)

        self.saveButton = QPushButton()
        self.saveButton.setText("Save to file")
        self.saveButton.clicked.connect(lambda: self.save_button_click(text))
        self.saveButton.setFocusPolicy(Qt.NoFocus)

        layoutV = QVBoxLayout()
        #layoutV.addWidget(self.imageLabel)
        layoutV.addWidget(self.scrollableLabel)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.copyButton)
        layoutH.addWidget(self.saveButton)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
    
    def copy_button_click(self, text):
        clipboard.copy(text.replace('\f',''))
    
    def save_button_click(self, text):
        #if file exists save text to it, if it doesn't then create and save. then exit
        saveFilePath = self.save_file_dialog()
        if saveFilePath:
            if(os.path.exists(saveFilePath)):
                saveFile = open(saveFilePath, "w")
                saveFile.write(text.replace('\f',''))
                saveFile.close()
            else:
                saveFile = open(saveFilePath, "x")
                saveFile.write(text.replace('\f',''))
                saveFile.close()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Save file","","Text Files (*.txt)", options=options)
        if fileName:
            return fileName



class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making widget resizable
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
 
        # creating label
        self.label = QLabel(content)
 
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)

        #making text selectable
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
 
        # adding label to the layout
        lay.addWidget(self.label)
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

def set_theme(app):
    app.setStyle("Fusion")

    theme_palette = QPalette()

    theme_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    theme_palette.setColor(QPalette.WindowText, Qt.white)
    theme_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    theme_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    theme_palette.setColor(QPalette.ToolTipBase, Qt.white)
    theme_palette.setColor(QPalette.ToolTipText, Qt.white)
    theme_palette.setColor(QPalette.Text, Qt.white)
    theme_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    theme_palette.setColor(QPalette.ButtonText, Qt.white)
    theme_palette.setColor(QPalette.BrightText, Qt.red)
    theme_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    theme_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    theme_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(theme_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    ss = screenshot.SnippingWidget()
    set_theme(app)
    window.show()
    sys.exit(app.exec_())

