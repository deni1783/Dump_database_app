from PyQt5 import QtWidgets, QtCore
import sys
from functools import partial
from Custom_modules.Main_window_classes.Work_template.SettingsBox import SettingsWindow
from Custom_modules.Main_window_classes.Work_template.ObjectTreeBox import ObjectTreeWindow
from Custom_modules.Main_window_classes.Work_template.LogBox import LogTextEdit
from Custom_modules.Functions.json_fn import add_or_change_default_objects, get_full_json_data, get_profile_settings_value
from Custom_modules.Functions.ui_fn import show_error_msg_window, change_cursor
from Custom_modules.Constants import PATH_TO_DEFAULT_OBJECTS_JSON, PATH_TO_PROFILE_SETTINGS_JSON, DIALECTS_FOR_CHANGE_DB_IN_QUERIES



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

        self.choose_default_obj_btn.clicked.connect(partial(self.load_default_objects,
                                                            PATH_TO_DEFAULT_OBJECTS_JSON,
                                                            PATH_TO_PROFILE_SETTINGS_JSON,
                                                            type_of_top_item,
                                                            dialect_name,
                                                            test_connection,
                                                            query_load_databases,
                                                            query_load_schemes,
                                                            query_load_tables
                                                            ))



    def save_as_default_object_list(self, path_to_json: str, top_lvl_item: str, dialect_name: str):
        curr_prof_name = self.profile_value_cmbb.currentText()
        selected_objects = self.get_selected_items(top_lvl_item)

        # Если не было выбранно ни одного объекта, ничего не делаем
        if not selected_objects:
            return
        add_or_change_default_objects(path_to_json, top_lvl_item, dialect_name, curr_prof_name, selected_objects)

    def load_default_objects(self, path_to_json: str,
                             path_to_profile_conn_settings: str,
                             top_lvl_item: str,
                             dialect_name: str,
                             test_connection,
                             query_load_databases,
                             query_load_schemes,
                             query_load_tables
                             ):
        """
        Полный трэш!!!
        Пробую объяснить.

        Проверяем есть ли сохраненные объекты для выбранного профиля, если нет, то окно ошибки
        Проверяем можно ли подключиться, если нет, то окно ошибки
        Очищаем верхний элемент дерева от детей
        Загружаем элементы верхнего уровня.
            Если top_lvl_item == 'database', то грузим и БАЗЫ и СХЕМЫ
                Есть проверка на подмену имени БД при подключении для диалектов из списка DIALECTS_FOR_CHANGE_DB_IN_QUERIES
            Если top_lvl_item == 'schema', то грузим СХЕМЫ

        Загружаем таблицы и делаем их статус чекбокса выбранными



        :param path_to_json: файл с сохраненными объектами для отображения
        :param path_to_profile_conn_settings: файл параметров подключения
        :param top_lvl_item: тип элемента верхнего уровня
        :param dialect_name: имя диалекта
        :param test_connection: фйнкция проверки соединения
        :param query_load_databases: функция получения БАЗ
        :param query_load_schemes: функция получения СХЕМ
        :param query_load_tables: функция получения ТАБЛИЦ
        :return: None
        """

        change_cursor('wait')

        curr_prof_name = self.profile_value_cmbb.currentText()
        full_json_data = get_full_json_data(path_to_json)

        # Если нет сохраненных объектов показываем окно ошибки и ничего не делаем
        if dialect_name not in full_json_data:
            show_error_msg_window('Empty objects list', 'There are no saved items for this dialect', self)
            change_cursor('normal')
            return
        if curr_prof_name not in full_json_data[dialect_name]:
            show_error_msg_window('Empty objects list', 'There are no saved items for this profile', self)
            change_cursor('normal')
            return


        profile_json_data = full_json_data[dialect_name][curr_prof_name]
        connection_settings = get_profile_settings_value(path_to_profile_conn_settings, dialect_name, curr_prof_name)

        # Проверяем возможность подлючиться с текущими параметрами
        try:
            test_connection(connection_settings)
        except:
            show_error_msg_window('Connection Error', sys.exc_info()[1].args[0], self)
            change_cursor('normal')
            return

        # Верхний элемент дерева
        parent_tree_obj = self.objects_tree.topLevelItem(0)

        # Очищаем дерево
        for c in range(parent_tree_obj.childCount()):
            parent_tree_obj.removeChild(parent_tree_obj.child(c))


        # Загружаем элементы верхнего уровня
        if top_lvl_item == 'database':
            databases_list = query_load_databases(connection_settings)

            # Добавляем БАЗЫ
            self.add_children_items(parent_tree_obj, databases_list)
            # Раскрываем элемент
            self.objects_tree.expandItem(parent_tree_obj)

            # Добавляем СХЕМЫ
            for i in range(parent_tree_obj.childCount()):
                database_item = parent_tree_obj.child(i)
                database_text = database_item.text(0)

                # Если БАЗА указана в сохранненом объекте, добавляем в нее СХЕМЫ
                if database_text in profile_json_data:

                    # Для диалектов из списка меняем БД для подключения
                    if dialect_name in DIALECTS_FOR_CHANGE_DB_IN_QUERIES:
                        connection_settings['database'] = database_text

                    schemes_list = query_load_schemes(connection_settings, database_text)
                    # Добавляем СХЕМЫ
                    self.add_children_items(database_item, schemes_list)
                    # Раскрываем элемент
                    self.objects_tree.expandItem(database_item)

        else:
            # top_lvl_item == 'schema':
            schemes_list = query_load_schemes(connection_settings)
            # Добавляем СХЕМЫ
            self.add_children_items(parent_tree_obj, schemes_list)
            # Раскрываем элемент
            self.objects_tree.expandItem(parent_tree_obj)





        # Добавляем ТАБЛИЦЫ для схем
        # Вынесен в отдельный цикл, т.к. количество детей в дереве изменилось и нужно обойти его сначала
        if top_lvl_item == 'database':
            for k in range(parent_tree_obj.childCount()):
                database_item = parent_tree_obj.child(k)
                database_text = database_item.text(0)

                if database_text in profile_json_data:

                    # Для диалектов из списка меняем БД для подключения
                    if dialect_name in DIALECTS_FOR_CHANGE_DB_IN_QUERIES:
                        connection_settings['database'] = database_text

                    for i in range(database_item.childCount()):
                        schema_item = database_item.child(i)
                        schema_text = schema_item.text(0)

                        # Если СХЕМА указана в сохранненом объекте, добавляем в нее ТАБЛИЦЫ
                        if schema_text in profile_json_data[database_text]:
                            table_list = query_load_tables(connection_settings, database_text, schema_text)
                            # Добавляем ТАБЛИЦЫ
                            self.add_children_items(schema_item, table_list)

                            # Делаем сохраненные таблицы выбранными
                            for j in range(schema_item.childCount()):
                                table_item = schema_item.child(j)
                                table_text = table_item.text(0)
                                if table_text in profile_json_data[database_text][schema_text]:
                                    table_item.setCheckState(0, QtCore.Qt.Checked)

                            # Раскрываем схемы
                            self.objects_tree.expandItem(schema_item)
        else:
            # top_lvl_item == 'schema':
            for k in range(parent_tree_obj.childCount()):
                schema_item = parent_tree_obj.child(k)
                schema_text = schema_item.text(0)
                # Если СХЕМА указана в сохранненом объекте, добавляем в нее ТАБЛИЦЫ
                if schema_text in profile_json_data:
                    # Пусто во втором параметре, т.к. он не участвует в запросе. Верхний уровень СХЕМА!
                    table_list = query_load_tables(connection_settings, '', schema_text)
                    # Добавляем ТАБЛИЦЫ
                    self.add_children_items(schema_item, table_list)

                    # Делаем сохраненные таблицы выбранными
                    for j in range(schema_item.childCount()):
                        table_item = schema_item.child(j)
                        table_text = table_item.text(0)
                        if table_text in profile_json_data[schema_text]:
                            table_item.setCheckState(0, QtCore.Qt.Checked)

                    # Раскрываем схемы
                    self.objects_tree.expandItem(schema_item)

        change_cursor('normal')
