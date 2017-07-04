from PyQt5 import QtWidgets
from Custom_modules.Constants import PATH_TO_PROFILE_SETTINGS_JSON
from Custom_modules.Main_window_classes.WorkTemplateBox import BaseWorkTemplateWindow
from Dialects.Queries import postgresql
from functools import partial


class WorkTemplate(BaseWorkTemplateWindow):
    def __init__(self):

        # Основные настройки для диалекта
        self.DIALECT_SETTINGS_OBJ = {
            'dialect_name': 'postgresql',
            'type_of_top_item': 'database',
            'test_connection': postgresql.check_connect,
            'query_load_databases': postgresql.load_databases,
            'query_load_schemes': postgresql.load_schemes,
            'query_load_tables': postgresql.load_tables
        }


        BaseWorkTemplateWindow.__init__(
            self,
            dialect_name=self.DIALECT_SETTINGS_OBJ['dialect_name'],
            type_of_top_item=self.DIALECT_SETTINGS_OBJ['type_of_top_item'],
            test_connection=self.DIALECT_SETTINGS_OBJ['test_connection'],
            query_load_databases=self.DIALECT_SETTINGS_OBJ['query_load_databases'],
            query_load_schemes=self.DIALECT_SETTINGS_OBJ['query_load_schemes'],
            query_load_tables=self.DIALECT_SETTINGS_OBJ['query_load_tables']
        )


        """ Обработка сигналов """
        # self.run_dump_btn.clicked.connect(partial(self.get_selected_items,
        #                                           self.DIALECT_SETTINGS_OBJ['type_of_top_item']
        #                                           ))
        #
        # # Проверка подключения (по нажатию кнопки TEST)
        # self.test_connect_btn.clicked.connect(partial(self.test_connection,
        #                                               PATH_TO_PROFILE_SETTINGS_JSON,
        #                                               self.DIALECT_SETTINGS_OBJ['dialect_name'],
        #                                               self.DIALECT_SETTINGS_OBJ['test_connection']
        #                                               ))

        # Возвращаем в основной макет
        self.out_dialect_gbox = self.work_template_out_gbox
