from PyQt5 import QtWidgets
from Custom_modules.Main_window_classes.WorkTemplateBox import BaseWorkTemplateWindow
from Dialects.Queries import postgresql

class WorkTemplate(BaseWorkTemplateWindow):
    def __init__(self):
        BaseWorkTemplateWindow.__init__(
            self,
            dialect_name='postgresql',
            type_of_top_item='database',
            test_connection=postgresql.check_connect,
            query_load_databases=postgresql.load_databases,
            query_load_schemes=postgresql.load_schemes,
            query_load_tables=postgresql.load_tables
        )



        # Возвращаем в основной макет
        self.out_dialect_gbox = self.work_template_out_gbox
