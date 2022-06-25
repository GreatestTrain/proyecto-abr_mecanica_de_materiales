import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Message 1", "Message 2"]
        self.button = QtWidgets.QPushButton("Button")
        self.text = QtWidgets.QLabel("Hello world", alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
	
if __name__=='__main__':
    app = QtWidgets.QApplication([])
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.resize(800,600)
    widget.show()
    sys.exit(app.exec())

