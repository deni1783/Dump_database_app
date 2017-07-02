from PyQt5 import QtWidgets



class RunDumButtons(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)


        """ Создаем виджеты кнопок """
        self.path_to_dir_btn = QtWidgets.QPushButton('Path to out dir')
        self.run_dump_btn = QtWidgets.QPushButton('Run creating DUMP')


        """ Представление для группировки кнопок """
        wrap_btns_hbox = QtWidgets.QHBoxLayout()

        # Добавляем кнопки
        wrap_btns_hbox.addWidget(self.path_to_dir_btn)
        wrap_btns_hbox.addWidget(self.run_dump_btn)

        """ Основной GBOX для отображения """
        self.run_dump_buttons_out_gbox = QtWidgets.QGroupBox()
        self.run_dump_buttons_out_gbox.setFlat(True)
        self.run_dump_buttons_out_gbox.setFixedHeight(50)
        self.run_dump_buttons_out_gbox.setLayout(wrap_btns_hbox)