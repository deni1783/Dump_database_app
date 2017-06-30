from PyQt5 import QtWidgets
from Custom_modules.Main_window_classes.Work_template.Settings_box.Connecting import Connecting


class WorkTemplate(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        test_vbox = QtWidgets.QVBoxLayout()
        test_lbl = Connecting('postgresql').out_gbox
        test_vbox.addWidget(test_lbl)

        # Возвращаем в основной макет
        self.out_dialect_gbox = QtWidgets.QGroupBox('postgresql')
        self.out_dialect_gbox.setLayout(test_vbox)
