from PyQt5 import QtWidgets
from functools import partial
from Custom_modules.Main_window_classes.DialectListBox import DialectListBox
from Custom_modules.Functions.ui_fn import clear_widget

from Dialects.UI_windows import postgresql


class ApplicationLayout(DialectListBox):
    def __init__(self, parent=None):
        DialectListBox.__init__(self, parent)

        # Словарь для присвоения нужных GBOX
        # При добавлении нового диалекта, необходимо добавить ссылку на GBOX для него
        self.dt_name_template = {
            'postgresql': postgresql.WorkTemplate().out_dialect_gbox
        }

        # Представление для рабочей области
        # Реализованно именно отдельным представлением, т.к. его необходимо очищать
        work_template_vbox = QtWidgets.QVBoxLayout()

        # Назначаем функцию для каждой кнопки
        for key in self.DIALECT_NAME_BTN:
            self.DIALECT_NAME_BTN[key].clicked.connect(partial(self.change_content, work_template_vbox, key))

        # Основное представление для приложения
        self.app_hbox = QtWidgets.QHBoxLayout()
        self.app_hbox.addLayout(self.dialects_list_vbox)
        self.app_hbox.addLayout(work_template_vbox)

        self.setLayout(self.app_hbox)

    def change_content(self, dist_layout, dt_name: str):
        """
        Функция сначала очищает, а потом добавляет GBOX виджет в dist_layout,
        :param dist_layout: представление в которое добавляем виджет
        :param dt_name: имя диалекта
        :return: None
        """
        print(dt_name)

        # Очищаем виджет
        clear_widget(dist_layout)

        # Делаем все кнопки диалектов активными
        for btn in self.DIALECT_NAME_BTN:
            self.DIALECT_NAME_BTN[btn].setDisabled(False)
        # Устанавливаем кнопку выбранного диалекта неактивной
        self.DIALECT_NAME_BTN[dt_name].setDisabled(True)

        # Получаем нужное представление для выбранного диалекта
        correct_gbox = self.get_correct_gbox(dt_name)

        # Записываем полученное представление в dist_layout
        dist_layout.addWidget(correct_gbox)

    def get_correct_gbox(self, dt_name: str):
        """
        Функция получения необходимого GBOX на основе словаря self.dt_name_template
        :param dt_name: имя диалекта
        :return: GBOX
        """

        # Проверяем что переданный диалект присутствует в словаре,
        # инаще возвращаем заглушку
        if dt_name.lower() in self.dt_name_template:
            return self.dt_name_template[dt_name.lower()]
        else:
            return QtWidgets.QGroupBox('Unsupported dialect: ' + dt_name)
