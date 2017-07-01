from PyQt5 import QtWidgets, QtCore
from Custom_modules.Main_window_classes.Work_template.Settings_box.Connecting import Connecting
from Custom_modules.Main_window_classes.Work_template.Settings_box.Dump import Dump


class SettingsWindow(Connecting, Dump):
    def __init__(self, dialect_name: str):
        Connecting.__init__(self, dialect_name)
        Dump.__init__(self, dialect_name)

        settings_wnd_vbox = QtWidgets.QVBoxLayout()
        settings_wnd_vbox.addWidget(self.connecting_settings_out_gbox)
        settings_wnd_vbox.addWidget(self.dump_settings_out_gbox)

        self.settings_window_out_gbox = QtWidgets.QGroupBox('Settings')
        self.settings_window_out_gbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.settings_window_out_gbox.setFlat(True)
        self.settings_window_out_gbox.setFixedWidth(302)

        self.settings_window_out_gbox.setLayout(settings_wnd_vbox)
