from PyQt5 import QtWidgets
from Custom_modules.Main_window_classes.WorkTemplateBox import BaseWorkTemplateWindow

class WorkTemplate(BaseWorkTemplateWindow):
    def __init__(self):
        BaseWorkTemplateWindow.__init__(self, 'postgresql')

        # Возвращаем в основной макет
        self.out_dialect_gbox = self.work_template_out_gbox
