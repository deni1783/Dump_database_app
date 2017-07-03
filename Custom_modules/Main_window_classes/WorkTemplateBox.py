from PyQt5 import QtWidgets, QtCore
from functools import partial
from Custom_modules.Main_window_classes.Work_template.SettingsBox import SettingsWindow
from Custom_modules.Main_window_classes.Work_template.ObjectTreeBox import ObjectTreeWindow
from Custom_modules.Main_window_classes.Work_template.LogBox import LogTextEdit
from Custom_modules.Functions.json_fn import add_or_change_default_objects
from Custom_modules.Constants import PATH_TO_DEFAULT_OBJECTS_JSON


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
                                  dialect_name,
                                  self.profile_value_cmbb,
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



        """ Обработка событий """
        self.save_as_default.clicked.connect(partial(self.save_as_default_object_list,
                                                     PATH_TO_DEFAULT_OBJECTS_JSON,
                                                     type_of_top_item,
                                                     dialect_name
                                                     ))

        self.choose_default_obj_btn.clicked.connect(partial(self.load_default_objects))



    def save_as_default_object_list(self, path_to_json: str, top_lvl_item: str, dialect_name: str):
        curr_prof_name = self.profile_value_cmbb.currentText()
        selected_objects = self.get_selected_items(top_lvl_item)

        # Если не было выбранно ни одного объекта, ничего не делаем
        if not selected_objects:
            return
        add_or_change_default_objects(path_to_json, top_lvl_item, dialect_name, curr_prof_name, selected_objects)

    def load_default_objects(self, path_to_json: str, top_lvl_item: str, dialect_name: str):
        curr_prof_name = self.profile_value_cmbb.currentText()