from PyQt5 import QtWidgets, QtCore


class LogTextEdit(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)


        """ Поле для вывода лога """
        self.log_area = QtWidgets.QTextEdit()
        self.log_area.setReadOnly(True)
