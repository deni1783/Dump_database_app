from PyQt5 import QtWidgets
from Custom_modules.Main_window_classes.Work_template.Settings_box.Connecting import Connecting
from Custom_modules.Main_window_classes.Work_template.Settings_box.Dump import Dump

class WorkTemplate(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        test_vbox = QtWidgets.QVBoxLayout()
        connecting_settings = Connecting('postgresql').out_gbox
        # dump_settings = Dump('postgresql').dump_settings_out_gbox
        dump_settings = Dump('postgresql')


        test_vbox.addWidget(connecting_settings)
        test_vbox.addWidget(dump_settings.dump_settings_out_gbox)

        # Возвращаем в основной макет
        self.out_dialect_gbox = QtWidgets.QGroupBox('postgresql')
        self.out_dialect_gbox.setLayout(test_vbox)
