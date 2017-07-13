from PyQt5 import QtWidgets, QtCore
from functools import partial
from Custom_modules.Main_window_classes.DialectListBox import DialectListBox
from Custom_modules.Functions.ui_fn import clear_widget
from Custom_modules.Main_window_classes.WorkTemplateBox import BaseWorkTemplateWindow

# Модули запросов для каждого диалекта
from Dialects.Queries import (postgresql, redshift, greenplum)

# Модули добавления уникальных виджетов
from Dialects.Custom_widgets import (custom_oracle, custom_postgresql)

# Модули функций обработки генерации дампов
from Dialects.Functions_for_geteration_dump import (run_dump_postgresql, run_dump_redshift, run_dump_greenplum)


class ApplicationLayout(DialectListBox):
    def __init__(self, parent=None):
        DialectListBox.__init__(self, parent)

        # Словарь для присвоения нужных параметров для создания интерфейса
        # При добавлении нового диалекта, необходимо добавить параметры для этого диалекта
        self.dt_name_template = {
            'postgresql': BaseWorkTemplateWindow(
                dialect_name='postgresql',
                type_of_top_item='database',
                fn_add_custom_widgets=custom_postgresql.add_custom_settings,
                test_connection=postgresql.check_connect,
                query_load_databases=postgresql.load_databases,
                query_load_schemes=postgresql.load_schemes,
                query_load_tables=postgresql.load_tables,
                func_for_prepare_dump=run_dump_postgresql.generate_dump
            ),

            'greenplum': BaseWorkTemplateWindow(
                dialect_name='greenplum',
                type_of_top_item='database',

                # Добавляем такие же уникальные виджеты как и для PostgreSQL
                fn_add_custom_widgets=custom_postgresql.add_custom_settings,

                test_connection=greenplum.check_connect,
                query_load_databases=greenplum.load_databases,
                query_load_schemes=greenplum.load_schemes,
                query_load_tables=greenplum.load_tables,
                func_for_prepare_dump=run_dump_greenplum.generate_dump
            ),

            'oracle': BaseWorkTemplateWindow(
                dialect_name='oracle',
                type_of_top_item='schema',
                fn_add_custom_widgets=custom_oracle.add_custom_settings,
                test_connection=postgresql.check_connect,
                query_load_databases=postgresql.load_databases,
                query_load_schemes=postgresql.load_schemes,
                query_load_tables=postgresql.load_tables,
                func_for_prepare_dump=None
            ),

            'redshift': BaseWorkTemplateWindow(
                dialect_name='redshift',
                type_of_top_item='schema',

                # Добавляем такие же уникальные виджеты как и для PostgreSQL
                fn_add_custom_widgets=custom_postgresql.add_custom_settings,

                test_connection=redshift.check_connect,
                query_load_databases=redshift.load_databases,
                query_load_schemes=redshift.load_schemes,
                query_load_tables=redshift.load_tables,
                func_for_prepare_dump=run_dump_redshift.generate_dump
            )
        }

        # Представление для рабочей области
        # Реализованно именно отдельным представлением, т.к. его необходимо очищать
        work_template_vbox = QtWidgets.QVBoxLayout()

        wrap_wort_template_gbox = QtWidgets.QGroupBox()
        wrap_wort_template_gbox.setFlat(True)
        wrap_wort_template_gbox.setLayout(work_template_vbox)

        # Назначаем функцию для каждой кнопки
        for key in self.DIALECT_NAME_BTN:
            self.DIALECT_NAME_BTN[key].clicked.connect(partial(self.change_content, work_template_vbox, key))

        """ Делаем изначально активной кнопку первого диалекта """
        # self.DIALECT_NAME_BTN[self.DIALECTS_LIST[0]].click()



        # Основное представление для приложения
        self.app_hbox = QtWidgets.QHBoxLayout()
        self.app_hbox.setAlignment(QtCore.Qt.AlignLeft)

        self.app_hbox.addWidget(self.dialect_list_gbox)
        self.app_hbox.addWidget(wrap_wort_template_gbox)

        self.setLayout(self.app_hbox)

    def change_content(self, dist_layout, dt_name: str):
        """
        Функция сначала очищает, а потом добавляет GBOX виджет в dist_layout,
        :param dist_layout: представление в которое добавляем виджет
        :param dt_name: имя диалекта
        :return: None
        """

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
            return self.dt_name_template[dt_name.lower()].work_template_out_gbox
        else:
            return QtWidgets.QGroupBox('Unsupported dialect: ' + dt_name)
