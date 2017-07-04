from PyQt5 import QtWidgets



class RunDumButtons(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)


        """ Создаем виджеты кнопок """
        self.choose_default_obj_btn = QtWidgets.QPushButton('Choose default objects')
        self.save_as_default = QtWidgets.QPushButton('Save as default')

        self.path_to_dir_btn = QtWidgets.QPushButton('Path to out dir')
        self.run_dump_btn = QtWidgets.QPushButton('Run creating DUMP')

        self.path_to_dir_value_txt = QtWidgets.QLineEdit()
        self.path_to_dir_value_txt.setReadOnly(True)
        self.path_to_dir_value_txt.hide()


        """ Представление для группировки кнопок GRID"""
        wrap_btns_grid = QtWidgets.QGridLayout()

        # Добавляем кнопки
        wrap_btns_grid.addWidget(self.choose_default_obj_btn, 0, 0)
        wrap_btns_grid.addWidget(self.save_as_default, 0, 1)

        wrap_btns_grid.addWidget(self.path_to_dir_btn, 1, 0)
        wrap_btns_grid.addWidget(self.run_dump_btn, 1, 1)

        wrap_btns_grid.addWidget(self.path_to_dir_value_txt, 2, 0, 1, 2)

        """ Основной GBOX для отображения """
        self.run_dump_buttons_out_gbox = QtWidgets.QGroupBox()
        self.run_dump_buttons_out_gbox.setFlat(True)
        # self.run_dump_buttons_out_gbox.setFixedHeight(90)
        self.run_dump_buttons_out_gbox.setLayout(wrap_btns_grid)