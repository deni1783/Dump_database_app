from PyQt5 import QtWidgets, QtCore
import sys
from functools import partial
from Custom_modules.Functions.json_fn import get_profile_settings_value
from Custom_modules.Functions.ui_fn import show_error_msg_window, change_cursor
from Custom_modules.Constants import PATH_TO_PROFILE_SETTINGS_JSON



class DatabaseObjectTree(QtWidgets.QWidget):
    def __init__(self,
                 dialect_name: str,
                 profile_value_cmbb,
                 top_lvl_item: str,
                 test_connection,
                 query_load_databases,
                 query_load_schemes,
                 query_load_tables):
        QtWidgets.QWidget.__init__(self)

        """ Создаем виджет дерева """
        self.objects_tree = QtWidgets.QTreeWidget()
        self.objects_tree.setMinimumWidth(500)

        self.objects_tree.setHeaderLabel('Objects')
        self.objects_tree.setSortingEnabled(True)
        self.objects_tree.sortByColumn(0, QtCore.Qt.AscendingOrder)  # Сортировка
        self.objects_tree.setAnimated(True)



        """ Добавляем элемент верхнего уровня в дерево"""
        top_item = QtWidgets.QTreeWidgetItem()
        top_item.setText(0, top_lvl_item)

        self.objects_tree.addTopLevelItem(top_item)


        wrap_tree_vbox = QtWidgets.QVBoxLayout()
        wrap_tree_vbox.addWidget(self.objects_tree)


        """ Создаем функции для обработки сигналов """

        def get_item_type(item, top_item: str):
            """
            Функция возвращает тип элемента дерева
            :param item: элемент дерева
            :param top_item: верхний элемент дерева
            :return: database or schema or table
            """

            """
            Получаем количество родителей для элемента
            0 - элемент верхнего уровня дерева (top_lvl_item)
            1 - database, schema
            2 - schema, table
            3 - table
            """
            test_item = item
            cnt_parent = 0
            while test_item is not None:
                test_item = test_item.parent()
                cnt_parent += 1
            # Что бы начинались с 0 отнимаем еденицу
            cnt_parent -= 1

            """
            Для того что бы совпадало количетсво родителей
            Получим:
            0 - элемент верхнего уровня дерева (top_lvl_item)
            1 - 
            2 - schema
            3 - table
            """
            if top_lvl_item == 'schema' and cnt_parent != 0:
                cnt_parent += 1

            if cnt_parent == 0 :
                return 'top_level'
            elif cnt_parent == 1:
                return 'database'
            elif cnt_parent == 2:
                return 'schema'
            elif cnt_parent == 3:
                return 'table'
            else:
                return 'unknown'

        def remove_children(parent_item):
            """
            Функция полностью очищает элемент дерева

            :param parent_item: элемент который очищаем
            :return: None
            """
            for i in reversed(range(parent_item.childCount())):
                parent_item.removeChild(parent_item.child(i))


        def add_children_items(parent_item, children: list):
            """
            Функция добавляет дочерние элементы в дерево

            :param parent_item: родительский элемент дерева в который добавляем детей
            :param children: массив элементов который добавляем
            :return: None
            """

            # Очищаем родитель от всех дочерних элементов
            remove_children(parent_item)

            # Добавляем детей
            for item in children:
                child = QtWidgets.QTreeWidgetItem(parent_item)
                child.setText(0, "{}".format(item))
                # child.setIcon(0, QtGui.QIcon("icons/{}.png".format(item_type)))
                child.setFlags(child.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                child.setCheckState(0, QtCore.Qt.Unchecked)

        def on_doubleclick_tree_item(tree, json_settings: str, load_db, load_schema, load_table):

            change_cursor('wait')

            # Получаем нажатый элемент, он является родителем
            curr_item = tree.currentItem()
            curr_item_text = curr_item.text(0)

            # Получаем тип нажатого элемента
            curr_item_type = get_item_type(curr_item, top_lvl_item)

            curr_profile = profile_value_cmbb.currentText()
            current_connection_settings = get_profile_settings_value(json_settings, dialect_name, curr_profile)




            # Выбираем нужную функцию и параметры к ней в зависимости от типа родителя
            # Когда curr_item_type == table or curr_item_type == unknown
            # children_arr остается пустым массивом и детей мы не добавляем

            # /Обрабатываем исключения для запросов
            try:
                children_arr = []
                if curr_item_type == 'top_level':
                    # Для диалектов у которого верхний уровень - БАЗА
                    if top_lvl_item == 'database':
                        # Загружием БАЗЫ
                        children_arr = load_db(current_connection_settings)

                    # Для диалектов у которого верхний уровень - СХЕМА
                    elif top_lvl_item == 'schema':
                        # Загружием СХЕМЫ
                        children_arr = load_schema(current_connection_settings, curr_item_text)

                # Для этих диалектов запросы необходимо запускать из друго БД,
                # для этого меняем значение DATABASE в строке подключения
                if dialect_name in ('postgresql', 'greenplum'):
                    current_connection_settings['database'] = curr_item_text

                if curr_item_type == 'database':
                    # Загружием СХЕМЫ
                    children_arr = load_schema(current_connection_settings, curr_item_text)

                elif curr_item_type == 'schema':
                    # Загружием ТАБЛИЦЫ
                    parent_db = curr_item.parent().text(0)
                    children_arr = load_table(current_connection_settings, parent_db, curr_item_text)

                if children_arr:
                    add_children_items(curr_item, children_arr)
            except:
                show_error_msg_window('Connection Error', sys.exc_info()[1].args[0], self)

            change_cursor('normal')


        """ Добавляем обработку событий """

        # При двойном нажатии на элемент дерева
        self.objects_tree.itemDoubleClicked.connect(partial(on_doubleclick_tree_item,
                                                            self.objects_tree,
                                                            PATH_TO_PROFILE_SETTINGS_JSON,
                                                            query_load_databases,
                                                            query_load_schemes,
                                                            query_load_tables
                                                            ))



        self.db_object_tree_out_box = QtWidgets.QGroupBox()
        self.db_object_tree_out_box.setLayout(wrap_tree_vbox)


    def get_selected_items(self, top_lvl_item: str):
        """
        Функция проходит все дерево и формирует массив со всеми выбранными элементами
        Глобальная функция!

        :param top_lvl_item: тип элемента верхнего уровня, для корректной обработки
        :return: list
        """

        all_children_arr = []

        # Получаем элемент верхнего уровня для всего дерева
        root = self.objects_tree.topLevelItem(0)

        # Обход всего дерева и заполнение массива all_children_arr
        for i in range(root.childCount()):
            first_item = root.child(i)
            if first_item.checkState(0) != 0:
                # Ключ для базы/схемы
                first_str = first_item.text(0)

                for j in range(first_item.childCount()):
                    second_item = first_item.child(j)
                    if second_item.checkState(0) != 0:
                        # Ключ для схемы/таблицы
                        second_str = second_item.text(0)

                        if second_item.childCount() != 0:
                            for k in range(second_item.childCount()):
                                third_item = second_item.child(k)
                                if third_item.checkState(0) != 0:
                                    # Ключ для таблицы
                                    third_str = third_item.text(0)
                                    all_children_arr.append(first_str + '.' + second_str + '.' + third_str)
                        elif top_lvl_item != 'database':
                            all_children_arr.append(first_str + '.' + second_str)

        return all_children_arr
