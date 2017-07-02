from PyQt5 import QtWidgets, QtCore


class Dump(QtWidgets.QWidget):
    def __init__(self, dialect_name: str, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        """ Создание виджетов """

        type_lbl = QtWidgets.QLabel('Type')

        """ Радио кнопки """
        data_radio = QtWidgets.QRadioButton('Data')
        data_radio.setChecked(True)

        schema_radio = QtWidgets.QRadioButton('Schema')
        full_radio = QtWidgets.QRadioButton('Full')

        self.DUMP_TYPE_RADIO_ARR = [data_radio, schema_radio, full_radio]



        """ Создание представлений """

        type_dump_hbox = QtWidgets.QHBoxLayout()




        """ Группировка виджетов в представления """
        type_dump_hbox.addWidget(type_lbl)
        type_dump_hbox.addWidget(data_radio)
        type_dump_hbox.addWidget(schema_radio)
        type_dump_hbox.addWidget(full_radio)



        """ Специальное представление для добавления уникальных настроек """
        self.custom_settings_for_dump_vbox = QtWidgets.QVBoxLayout()
        self.custom_settings_for_dump_vbox.setAlignment(QtCore.Qt.AlignTop)


        """ Обертка для сгруппированных представлений (VBOX) """
        wrap_dump_setting_vbox = QtWidgets.QVBoxLayout()
        wrap_dump_setting_vbox.setAlignment(QtCore.Qt.AlignTop)
        wrap_dump_setting_vbox.addLayout(type_dump_hbox)
        wrap_dump_setting_vbox.addLayout(self.custom_settings_for_dump_vbox)



        """ Основной группирированный бокс (GBOX) """
        self.dump_settings_out_gbox = QtWidgets.QGroupBox('Dump settings')
        self.dump_settings_out_gbox.setAlignment(QtCore.Qt.AlignCenter)
        self.dump_settings_out_gbox.setFlat(True)
        self.dump_settings_out_gbox.setFixedWidth(300)

        self.dump_settings_out_gbox.setLayout(wrap_dump_setting_vbox)

    # Получить выбранный тип дампа
    def get_checked_type_dump_radio(self):
        """
        Функция определяет выбранный тип дампв
        :return: str (имя выбранного типа дампа)
        """
        for r in range(len(self.DUMP_TYPE_RADIO_ARR)):
            if self.DUMP_TYPE_RADIO_ARR[r].isChecked():
                return self.DUMP_TYPE_RADIO_ARR[r].text()

