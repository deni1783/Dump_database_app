from PyQt5 import QtWidgets, QtCore
from Custom_modules.Main_window_classes.Work_template.Object_tree_box.DatabaseObjects import DatabaseObjectTree
from Custom_modules.Main_window_classes.Work_template.Object_tree_box.RunButtons import RunDumButtons


class ObjectTreeWindow(DatabaseObjectTree, RunDumButtons):
    def __init__(self,
                 top_lvl_item: str,
                 test_connection,
                 query_load_databases,
                 query_load_schemes,
                 query_load_tables):
        DatabaseObjectTree.__init__(self,
                                    top_lvl_item,
                                    test_connection,
                                    query_load_databases,
                                    query_load_schemes,
                                    query_load_tables)
        RunDumButtons.__init__(self)

        """ Группировка представлений """
        wrap_vbox = QtWidgets.QVBoxLayout()

        # Дерево
        wrap_vbox.addWidget(self.db_object_tree_out_box)

        # Кнопки управления дампа
        wrap_vbox.addWidget(self.run_dump_buttons_out_gbox)



        """ Базовий GBOX для приложения """
        self.object_tree_window_out_gbox = QtWidgets.QGroupBox('Objects')
        self.object_tree_window_out_gbox.setFlat(True)
        self.object_tree_window_out_gbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.object_tree_window_out_gbox.setLayout(wrap_vbox)