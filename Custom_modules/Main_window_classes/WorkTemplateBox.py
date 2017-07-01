from PyQt5 import QtWidgets, QtCore
from Custom_modules.Main_window_classes.Work_template.SettingsBox import SettingsWindow
from Custom_modules.Main_window_classes.Work_template.ObjectTreeBox import ObjectTreeWindow


class BaseWorkTemplateWindow(SettingsWindow, ObjectTreeWindow):
    def __init__(self,
                 dialect_name: str,
                 type_of_top_item: str,
                 test_connection,
                 query_load_databases,
                 query_load_schemes,
                 query_load_tables):

        SettingsWindow.__init__(self, dialect_name)

        ObjectTreeWindow.__init__(self,
                                  type_of_top_item,
                                  test_connection,
                                  query_load_databases,
                                  query_load_schemes,
                                  query_load_tables)


        """ Группировка основных представлений """
        work_template_hbox = QtWidgets.QHBoxLayout()

        # Окно настроек
        work_template_hbox.addWidget(self.settings_window_out_gbox)
        work_template_hbox.addWidget(self.db_object_tree_out_box)


        """ Базовий GBOX для приложения """
        self.work_template_out_gbox = QtWidgets.QGroupBox(dialect_name)
        self.work_template_out_gbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.work_template_out_gbox.setFlat(True)

        self.work_template_out_gbox.setLayout(work_template_hbox)
