import sys
from PyQt5.Qt import *
import find_files
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

        vbox = QVBoxLayout()
        inbox = QHBoxLayout()
        inbox.addWidget(self.browseBut)
        inbox.addWidget(self.path_line)
        vbox.addLayout(inbox)
        vbox.addStretch(1)

        checkBox = QHBoxLayout()
        checkBoxLeft = QVBoxLayout()
        checkBoxRight = QVBoxLayout()

        black_and_white = QCheckBox('Black and white', self)
        black_and_white.stateChanged.connect(self.treat_black_white)
        noises = QCheckBox('Noises', self)
        noises.stateChanged.connect(self.treat_noises)
        turns = QCheckBox('Turn', self)
        turns.stateChanged.connect(self.treat_turns)
        gray_shades = QCheckBox('Shades gray', self)
        gray_shades.stateChanged.connect(self.treat_gray_shades)
        strips = QCheckBox('Strips', self)
        strips.stateChanged.connect(self.treat_strip)

        glare = QCheckBox('Glares', self)
        glare.stateChanged.connect(self.treat_glare)
        blur = QCheckBox('Blur', self)
        blur.stateChanged.connect(self.treat_blur)
        compress = QCheckBox('Compress', self)
        compress.stateChanged.connect(self.treat_compress)
        stretch = QCheckBox('Stretch', self)
        stretch.stateChanged.connect(self.treat_stretch)


        checkBoxLeft.addWidget(black_and_white)
        checkBoxLeft.addWidget(noises)
        checkBoxLeft.addWidget(turns)
        checkBoxLeft.addWidget(gray_shades)
        checkBoxLeft.addWidget(strips)

        checkBoxRight.addWidget(glare)
        checkBoxRight.addWidget(blur)
        checkBoxRight.addWidget(compress)
        checkBoxRight.addWidget(stretch)

        checkBox.addLayout(checkBoxLeft)
        checkBox.addLayout(checkBoxRight)
        vbox.addLayout(checkBox)
        vbox.addWidget(self.runBut)

        self.setLayout(vbox)
        self.show()
        self.move(250, 150)
        self.setWindowTitle('Program')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()

    def treat_black_white(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([1])
            self.showDialog(1)
        else:
            self.remove_value(1)
    def treat_noises(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([2])
            self.showDialog(2)
        else:
            self.remove_value(2)
    def treat_turns(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([3])
            self.showDialog(3)
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
            self.showDialog(5)
        else:
            self.remove_value(5)
    def treat_glare(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([6])
            self.showDialog(6)
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
            self.showDialog(8)
        else:
            self.remove_value(8)
    def treat_stretch(self, state):
        if state == Qt.Checked:
            self.arr_treat.append([9])
            self.showDialog(9)
        else:
            self.remove_value(9)
    def remove_value(self, x):
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

    def showDialog(self, treat):
        value, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter conversion factor:')

        if ok:
            x = self.arr_treat.index([treat])
            self.arr_treat[x].append(int(value))

    def runClicked(self):
        if not self.DIRPATH == '':
            find_files.be(self.DIRPATH, self.arr_treat)
            self.path_line.clear()
            self.DIRPATH = ''
            print(self.arr_treat)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(500, 171)
    sys.exit(app.exec_())