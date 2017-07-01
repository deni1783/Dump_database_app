from PyQt5 import QtWidgets, QtCore
from Custom_modules.Main_window_classes.Work_template.SettingsBox import SettingsWindow


class BaseWorkTemplateWindow(SettingsWindow):
    def __init__(self, dialect_name: str):
        SettingsWindow.__init__(self, dialect_name)


        """ Группировка основных представлений """
        work_template_hbox = QtWidgets.QHBoxLayout()

        # Окно настроек
        work_template_hbox.addWidget(self.settings_window_out_gbox)


        """ Базовий GBOX для приложения """
        self.work_template_out_gbox = QtWidgets.QGroupBox(dialect_name)
        self.work_template_out_gbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.work_template_out_gbox.setFlat(True)

        self.work_template_out_gbox.setLayout(work_template_hbox)
