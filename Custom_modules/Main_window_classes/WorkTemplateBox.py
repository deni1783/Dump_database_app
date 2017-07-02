from PyQt5 import QtWidgets, QtCore
from Custom_modules.Main_window_classes.Work_template.SettingsBox import SettingsWindow
from Custom_modules.Main_window_classes.Work_template.ObjectTreeBox import ObjectTreeWindow
from Custom_modules.Main_window_classes.Work_template.LogBox import LogTextEdit


class BaseWorkTemplateWindow(SettingsWindow, ObjectTreeWindow, LogTextEdit):
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

        LogTextEdit.__init__(self)


        """ Группировка основных представлений Настроки и Дерево в HBOX"""
        work_template_hbox = QtWidgets.QHBoxLayout()

        # Окно настроек
        work_template_hbox.addWidget(self.settings_window_out_gbox)
        # Окно дерева
        work_template_hbox.addWidget(self.object_tree_window_out_gbox)


        """ Добавляем work_template_hbox в GBOX """
        wrap_top_wnd = QtWidgets.QGroupBox()
        wrap_top_wnd.setLayout(work_template_hbox)



        """ Обертка для рабочей области включает Настройки, Дерево и Лог SPLITTER """
        wrap_work_template_splitter = QtWidgets.QSplitter()
        wrap_work_template_splitter.setOrientation(QtCore.Qt.Vertical)

        # Верхнее окно (Настройки и Дерево)
        wrap_work_template_splitter.addWidget(wrap_top_wnd)
        # Окно лога
        wrap_work_template_splitter.addWidget(self.log_area)



        """ Добавляем SPLITTER в HBOX """
        full_wrap = QtWidgets.QHBoxLayout()
        full_wrap.addWidget(wrap_work_template_splitter)



        """ Базовий GBOX для приложения """
        self.work_template_out_gbox = QtWidgets.QGroupBox(dialect_name)
        self.work_template_out_gbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.work_template_out_gbox.setFlat(True)

        self.work_template_out_gbox.setLayout(full_wrap)
