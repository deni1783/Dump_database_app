from PyQt5 import QtWidgets
from Custom_modules.Main_window_classes.Work_template.Object_tree_box.DatabaseObjects import DatabaseObjectTree



class ObjectTreeWindow(DatabaseObjectTree):
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
