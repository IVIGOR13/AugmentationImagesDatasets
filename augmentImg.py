import sys
from PyQt5.Qt import *
import os
import treatment_images as ti
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.DIRPATH = ''
        self.arr_treat = []
        self.initUI()

    def initUI(self):
        self.browseBut = QPushButton("Browse")
        self.runBut = QPushButton("Run")
        self.browseBut.clicked.connect(self.browseClicked)
        self.runBut.clicked.connect(self.runClicked)

        self.path_line = QLineEdit(self)
        self.path_line.textChanged[str].connect(self.onChangeBrowseLine)

        inbox = QHBoxLayout()
        inbox.addWidget(self.browseBut)
        inbox.addWidget(self.path_line)

        # 1
        checkBox = QHBoxLayout()
        checkBoxLeft = QVBoxLayout()
        checkBoxRight = QVBoxLayout()

        # Left column
        self.black_and_white = QCheckBox('Black and white', self)
        self.noises = QCheckBox('Noises', self)
        self.turns = QCheckBox('Turn', self)
        self.gray_shades = QCheckBox('Shades gray', self)
        self.strips = QCheckBox('Strips', self)

        self.black_and_white.stateChanged.connect(self.treat_black_white)
        self.noises.stateChanged.connect(self.treat_noises)
        self.turns.stateChanged.connect(self.treat_turns)
        self.gray_shades.stateChanged.connect(self.treat_gray_shades)
        self.strips.stateChanged.connect(self.treat_strip)

        # Right column
        self.glare = QCheckBox('Glares', self)
        self.blur = QCheckBox('Blur', self)
        self.compress = QCheckBox('Compress', self)
        self.stretch = QCheckBox('Stretch', self)

        self.glare.stateChanged.connect(self.treat_glare)
        self.blur.stateChanged.connect(self.treat_blur)
        self.compress.stateChanged.connect(self.treat_compress)
        self.stretch.stateChanged.connect(self.treat_stretch)

        checkBoxLeft.addWidget(self.black_and_white)
        checkBoxLeft.addWidget(self.noises)
        checkBoxLeft.addWidget(self.turns)
        checkBoxLeft.addWidget(self.gray_shades)
        checkBoxLeft.addWidget(self.strips)

        checkBoxRight.addWidget(self.glare)
        checkBoxRight.addWidget(self.blur)
        checkBoxRight.addWidget(self.compress)
        checkBoxRight.addWidget(self.stretch)

        checkBox.addLayout(checkBoxLeft)
        checkBox.addLayout(checkBoxRight)

        #2
        checkBox_one = QHBoxLayout()
        checkBoxLeft_one = QVBoxLayout()
        checkBoxRight_one = QVBoxLayout()

        # Left column
        self.black_and_white_one = QCheckBox('Black and white', self)
        self.noises_one = QCheckBox('Noises', self)
        self.turns_one = QCheckBox('Turn', self)
        self.gray_shades_one = QCheckBox('Shades gray', self)
        self.strips_one = QCheckBox('Strips', self)

        self.black_and_white_one.stateChanged.connect(self.treat_black_white)
        self.noises_one.stateChanged.connect(self.treat_noises)
        self.turns_one.stateChanged.connect(self.treat_turns)
        self.gray_shades_one.stateChanged.connect(self.treat_gray_shades)
        self.strips_one.stateChanged.connect(self.treat_strip)

        # Right column
        self.glare_one = QCheckBox('Glares', self)
        self.blur_one = QCheckBox('Blur', self)
        self.compress_one = QCheckBox('Compress', self)
        self.stretch_one = QCheckBox('Stretch', self)

        self.glare_one.stateChanged.connect(self.treat_glare)
        self.blur_one.stateChanged.connect(self.treat_blur)
        self.compress_one.stateChanged.connect(self.treat_compress)
        self.stretch_one.stateChanged.connect(self.treat_stretch)

        checkBoxLeft_one.addWidget(self.black_and_white_one)
        checkBoxLeft_one.addWidget(self.noises_one)
        checkBoxLeft_one.addWidget(self.turns_one)
        checkBoxLeft_one.addWidget(self.gray_shades_one)
        checkBoxLeft_one.addWidget(self.strips_one)

        checkBoxRight_one.addWidget(self.glare_one)
        checkBoxRight_one.addWidget(self.blur_one)
        checkBoxRight_one.addWidget(self.compress_one)
        checkBoxRight_one.addWidget(self.stretch_one)

        checkBox_one.addLayout(checkBoxLeft_one)
        checkBox_one.addLayout(checkBoxRight_one)

        tab1 = QFrame()
        tab1.setLayout(checkBox)
        tab2 = QFrame()
        tab2.setLayout(checkBox_one)
        self.tab = QTabWidget()
        self.tab.addTab(tab1, "&more")
        self.tab.addTab(tab2, "&one")
        self.tab.currentChanged.connect(self.changeTab)

        vbox = QVBoxLayout()
        vbox.addLayout(inbox)
        vbox.addWidget(self.tab)
        vbox.addWidget(self.runBut)

        self.setLayout(vbox)
        self.show()
        self.move(250, 150)
        self.setWindowTitle('AugmentationImg')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()

    def changeTab(self):
        self.arr_treat = []

    def treat_black_white(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([1])
            self.showDialog(1, 'Change the conversion threshold.')
        else:
            self.remove_value(1)
    def treat_noises(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([2])
            self.showDialog(2, 'Noise factor.')
        else:
            self.remove_value(2)
    def treat_turns(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([3])
            self.showDialog(3, 'Rotate in degrees.')
        else:
            self.remove_value(3)
    def treat_gray_shades(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([4])
        else:
            self.remove_value(4)
    def treat_strip(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([5])
            self.showDialog(5, 'How many tones to shade.')
        else:
            self.remove_value(5)
    def treat_glare(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([6])
            self.showDialog(6, 'How many tones to shade.')
        else:
            self.remove_value(6)
    def treat_blur(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([7])
        else:
            self.remove_value(7)
    def treat_compress(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([8])
            self.showDialog(8, 'How many times to compress.')
        else:
            self.remove_value(8)
    def treat_stretch(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([9])
            self.showDialog(9, 'How many times to stretch.')
        else:
            self.remove_value(9)
    def remove_value(self, x):
        if not self.arr_treat == []:
            for i in [0, 1, 2, 4, 5, 7, 8]:
                if self.arr_treat[i][0] == x:
                    self.arr_treat.__delitem__(i)
                    break

    def onChangeBrowseLine(self, text):
        self.DIRPATH = text

    def browseClicked(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.DIRPATH = path
        self.path_line.setText(self.DIRPATH)

    def showDialog(self, treat, text):
        value, ok = QInputDialog.getText(self, 'Input Dialog',  str(text) + '\nEnter conversion factor:')

        if ok:
            if value != '':
                x = self.arr_treat.index([treat])
                self.arr_treat[x].append(float(value))

    def runClicked(self):
        if not self.DIRPATH == '':
            files = os.listdir(self.DIRPATH)
            images_png = [x for x in files if x.endswith('.png')]
            images_jpg = [x for x in files if x.endswith('.jpg')]
            images = images_png + images_jpg
            for i in images:
                ti.TreatmentImages(self.DIRPATH, i, self.arr_treat, self.tab.currentIndex())

            self.path_line.clear()
            self.DIRPATH = ''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(630, 171)
    sys.exit(app.exec_())
