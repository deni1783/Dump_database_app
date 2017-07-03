from PyQt5 import QtWidgets, QtCore
from functools import partial
# from Custom_modules.Constants import PATH_TO_PROFILE_SETTINGS_JSON
from Custom_modules.Functions.json_fn import write_new_profile_to_json
from Custom_modules.Functions.ui_fn import show_error_msg_window

class AddingNewProfileWindow(QtWidgets.QWidget):
    """
        Класс создает окно для добавления нового профиля настроек подлючения
    """
    def __init__(self, parent, path_to_json: str, dialect_name: str, change_list_profile_func):
        QtWidgets.QWidget.__init__(self)

        """ Заголовки для параметров подключения """
        new_profile_lbl = QtWidgets.QLabel('New profile')

        host_lbl = QtWidgets.QLabel('HOST')
        port_lbl = QtWidgets.QLabel('PORT')
        database_lbl = QtWidgets.QLabel('DATABASE')
        user_lbl = QtWidgets.QLabel('USER')
        password_lbl = QtWidgets.QLabel('PASSWORD')

        """ Значения параметров подключения """
        new_profile_value_ln = QtWidgets.QLineEdit()

        host_value_ln = QtWidgets.QLineEdit()
        port_value_ln = QtWidgets.QLineEdit()
        database_value_ln = QtWidgets.QLineEdit()
        user_value_ln = QtWidgets.QLineEdit()
        password_value_ln = QtWidgets.QLineEdit()

        """ Кнопки управления """
        save_btn = QtWidgets.QPushButton('Save')
        cancel_btn = QtWidgets.QPushButton('Cancel')

        """ Параметры подключения (GRID) """
        connecting_string_grid = QtWidgets.QGridLayout()
        connecting_string_grid.setAlignment(QtCore.Qt.AlignTop)

        """ Представления для группировки кнопок управления (HBOX) """
        btns_hbox = QtWidgets.QHBoxLayout()

        """ Основное представления (VBOX) """
        wrap_vbox = QtWidgets.QVBoxLayout()



        """ Группировка параметров подключения """
        # Новый профиль
        connecting_string_grid.addWidget(new_profile_lbl, 0, 0)
        connecting_string_grid.addWidget(new_profile_value_ln, 0, 1)
        # host
        connecting_string_grid.addWidget(host_lbl, 1, 0)
        connecting_string_grid.addWidget(host_value_ln, 1, 1)
        # port
        connecting_string_grid.addWidget(port_lbl, 2, 0)
        connecting_string_grid.addWidget(port_value_ln, 2, 1)
        # database
        connecting_string_grid.addWidget(database_lbl, 3, 0)
        connecting_string_grid.addWidget(database_value_ln, 3, 1)
        # user
        connecting_string_grid.addWidget(user_lbl, 4, 0)
        connecting_string_grid.addWidget(user_value_ln, 4, 1)
        # password
        connecting_string_grid.addWidget(password_lbl, 5, 0)
        connecting_string_grid.addWidget(password_value_ln, 5, 1)


        """ Группируем кнопки управления """
        btns_hbox.addWidget(save_btn)
        btns_hbox.addWidget(cancel_btn)

        """ Группируем в одно представления """
        wrap_vbox.addLayout(connecting_string_grid)
        wrap_vbox.addLayout(btns_hbox)


        """ Окно добавления нового профиля """
        self.create_profile_wnd = QtWidgets.QWidget()
        self.create_profile_wnd.setWindowFlags(QtCore.Qt.Tool)
        self.create_profile_wnd.setWindowTitle('New profile')

        self.create_profile_wnd.setLayout(wrap_vbox)


        """ Вспомогательные функции """
        def get_settings():
            """
            Функция обрабатывает введенные значения и возвращает эти значения

            :return: dict
            """
            settings_obj = {
                'new_profile_name': new_profile_value_ln.text(),
                'host': host_value_ln.text(),
                'port': port_value_ln.text(),
                'database': database_value_ln.text(),
                'user': user_value_ln.text(),
                'password': password_value_ln.text()
            }

            return settings_obj


        """ Объявление функции для обработки нажатий """
        def saved_new_profile(parent):
            """
            Функция сохраняет введенные значения для нового профиля в файл connection_profiles.json

            :param parent: родитель для окна ошибки
            :return: None
            """
            # Получаем новые настройки
            new_settings = get_settings()

            # Проверяем что HOST, USER и new_profile_name заполнены
            if not new_settings['new_profile_name'] or not new_settings['host'] or not new_settings['port']:
                err_msg = ''
                if not new_settings['new_profile_name']:
                    err_msg += 'The field "New profile" is not filled!\n'
                if not new_settings['host']:
                    err_msg += 'The field "HOST" is not filled!\n'
                if not new_settings['port']:
                    err_msg += 'The field "PORT" is not filled!\n'

                # Показываем окно ошибки и завершаем функцию
                show_error_msg_window('Fields of the form are not filled', err_msg, parent)
                return

            # Записываем настройки в файл
            write_new_profile_to_json(path_to_json, dialect_name, new_settings)

            # Перезаписываем значения в combo box
            change_list_profile_func(path_to_json, dialect_name)

            # Закрываем окно
            self.create_profile_wnd.close()

        def cancel():
            # Закрываем окно
            self.create_profile_wnd.close()


        """ Обработка нажатий на кнопки """

        # Сохранить новый профиль
        save_btn.clicked.connect(partial(saved_new_profile, parent))

        # Отменить
        cancel_btn.clicked.connect(partial(cancel))
