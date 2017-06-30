from PyQt5 import QtWidgets


class WorkTemplate(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        test_vbox = QtWidgets.QVBoxLayout()
        test_lbl = QtWidgets.QLabel('test lbl for postgresql')
        test_vbox.addWidget(test_lbl)

        # Возвращаем в основной макет
        self.out_dialect_gbox = QtWidgets.QGroupBox('postgresql')
        self.out_dialect_gbox.setLayout(test_vbox)
