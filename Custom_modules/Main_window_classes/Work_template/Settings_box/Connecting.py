from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from Custom_modules.Functions.json_fn import get_profile_settings_value
from Custom_modules.Functions.json_fn import get_all_profiles
from Custom_modules.Functions.json_fn import del_profile_from_json
from Custom_modules.Constants import PATH_TO_PROFILE_SETTINGS_JSON

from Custom_modules.Main_window_classes.Work_template.Settings_box.AddProfileWnd import AddingNewProfileWindow



class Connecting(QtWidgets.QWidget):
    def __init__(self, dialect_name: str, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        """ Создание виджетов """

        """ Профиль """
        profile_lbl = QtWidgets.QLabel('Current profile:')
        profile_value_cmbb = QtWidgets.QComboBox()

        """ Кнопки настройки профиля """
        add_profile_btn = QtWidgets.QPushButton('ADD')
        delete_profile_btn = QtWidgets.QPushButton('DEL')
        edit_profile_btn = QtWidgets.QPushButton('EDIT')

        """ Кнопка проверки подключения """
        test_connect_btn = QtWidgets.QPushButton('TEST')

        """ Статус подключения (LABEL)"""
        status_lbl = QtWidgets.QLabel()
        # Сначала делаем описание - Not yet tested
        status_lbl.setToolTip('Not yet tested')

        """ Icons для статуса подключения PIXMAP """
        success_pix = QtGui.QPixmap("Img/Icons/success.png")
        error_pix = QtGui.QPixmap("Img/Icons/error.png")
        question_pix = QtGui.QPixmap("Img/Icons/question.png")





        """ Пустой виджет, для отступа """
        empty_lbl = QtWidgets.QLabel()

        """ Заголовки для параметров подключения """
        host_lbl = QtWidgets.QLabel('HOST')
        port_lbl = QtWidgets.QLabel('PORT')
        database_lbl = QtWidgets.QLabel('DATABASE')
        user_lbl = QtWidgets.QLabel('USER')
        password_lbl = QtWidgets.QLabel('PASSWORD')

        """ Значения параметров подключения """
        host_value_ln = QtWidgets.QLineEdit()
        port_value_ln = QtWidgets.QLineEdit()
        database_value_ln = QtWidgets.QLineEdit()
        user_value_ln = QtWidgets.QLineEdit()
        password_value_ln = QtWidgets.QLineEdit()

        # Устанавливаем текстовые поля ReadOnly
        host_value_ln.setReadOnly(True)
        port_value_ln.setReadOnly(True)
        database_value_ln.setReadOnly(True)
        user_value_ln.setReadOnly(True)
        password_value_ln.setReadOnly(True)




        """ Создание представлений для группировки """

        """ Профиль (HBOX) """
        profile_hbox = QtWidgets.QHBoxLayout()

        """ Кнопки настройки профиля (GRID) """
        profile_buttons_grid = QtWidgets.QGridLayout()

        """ Параметры подключения (GRID) """
        connecting_string_grid = QtWidgets.QGridLayout()




        """ Группировка профиля """
        profile_hbox.addWidget(profile_lbl)
        profile_hbox.addWidget(profile_value_cmbb)

        """ Группировка кнопок настройки профиля """
        profile_buttons_grid.addWidget(add_profile_btn, 0 ,0)
        profile_buttons_grid.addWidget(delete_profile_btn, 0, 1)
        profile_buttons_grid.addWidget(edit_profile_btn, 0, 2)
        # + кнопка тестирования соединения
        profile_buttons_grid.addWidget(empty_lbl, 0, 3)
        profile_buttons_grid.addWidget(test_connect_btn, 0, 4)

        # Изначально делаем статус неопределенным
        status_lbl.setPixmap(question_pix)
        profile_buttons_grid.addWidget(status_lbl, 0, 5)




        """ Группировка параметров подключения """
        # host
        connecting_string_grid.addWidget(host_lbl, 0, 0)
        connecting_string_grid.addWidget(host_value_ln, 0, 1)
        # port
        connecting_string_grid.addWidget(port_lbl, 1, 0)
        connecting_string_grid.addWidget(port_value_ln, 1, 1)
        # database
        connecting_string_grid.addWidget(database_lbl, 2, 0)
        connecting_string_grid.addWidget(database_value_ln, 2, 1)
        # user
        connecting_string_grid.addWidget(user_lbl, 3, 0)
        connecting_string_grid.addWidget(user_value_ln, 3, 1)
        # password
        connecting_string_grid.addWidget(password_lbl, 4, 0)
        connecting_string_grid.addWidget(password_value_ln, 4, 1)




        """ Обертка для сгруппированных представлений (VBOX) """
        wrap_connect_settings_vbox = QtWidgets.QVBoxLayout()
        wrap_connect_settings_vbox.addLayout(profile_hbox)
        wrap_connect_settings_vbox.addLayout(connecting_string_grid)
        wrap_connect_settings_vbox.addLayout(profile_buttons_grid)




        """ Основной группирированный бокс (GBOX) """
        self.out_gbox = QtWidgets.QGroupBox('Connection settings')
        self.out_gbox.setAlignment(QtCore.Qt.AlignCenter)
        self.out_gbox.setFlat(True)
        # self.out_gbox.setFixedSize(400, 400)
        self.out_gbox.setFixedSize(300, 280)
        self.out_gbox.setLayout(wrap_connect_settings_vbox)






        """ Функции для работы с профилями """

        # Переопределяем параметры подключения, на основе выбранного профиля
        def change_profile_settings_values(new_settings: dict):
            """
            Функция перезаписивает значения параметров подключения
            :param new_settings: объект с новыми значениями
            :return: None
            """
            host_value_ln.setText(new_settings['host'])
            port_value_ln.setText(new_settings['port'])
            database_value_ln.setText(new_settings['database'])
            user_value_ln.setText(new_settings['user'])
            password_value_ln.setText(new_settings['password'])

        # При изменении активированного профиля
        def change_profile(path_to_json: str, dt_name: str, new_prof: str):
            """
            Функция перерисовывает параметры подкючения при изменении профиля
            Парсит файл Settings/connection_profiles.json

            :param path_to_json: путь к файлу профилей подключения
            :param dt_name: имя диалекта, что бы найти корректные значения для профиля
            :param new_prof: имя нового профиля
            :return: None
            """

            # Заполнаем объект новыми значениями из полученного профиля
            new_prof_settings = get_profile_settings_value(path_to_json, dt_name, new_prof)

            # Перезаписываем старые значения новыми
            change_profile_settings_values(new_prof_settings)

        # Заполнение названий профилей
        def init_start_profile_values(path_to_json: str, dt_name: str):
            """
            Функция перезаписывает все значения профиля в profile_value_cmbb
            А также устанавливает для активированного профиля его параметры подключения

            :param path_to_json: файл с профилями подключения
            :param dt_name: диалект для которого ище профили
            :return: None
            """

            # Записуем в массив список полученных профилей
            profile_list = get_all_profiles(path_to_json, dt_name)

            # Очищаем список профилей из combo box (profile_value_cmbb)
            profile_value_cmbb.clear()

            # Добавляем новые значения в combo box (profile_value_cmbb)
            for i in sorted(profile_list):
                profile_value_cmbb.addItem(i)

            curr_prof = profile_value_cmbb.currentText()
            change_profile(path_to_json, dt_name, curr_prof)

        # Показываем окно создания нового профиля
        def show_create_new_prof_window(path_to_json: str, dt_name: str, init_new_pfofiles_func):
            """
            Функция получает класс создания нового профиля и показывает его

            :param dt_name: имя диалекта, что бы коррекно записать профиль
            :param parent: Родительский компонент для которого показываем окно
            :param path_to_json: путь к файлу настроек подключения, что бы записать новые настройки
            :return: None
            """
            new_prof_window = AddingNewProfileWindow(path_to_json, dt_name, init_new_pfofiles_func)
            new_prof_window.create_profile_wnd.show()

        def del_curr_profile(json_file: str, dt_name: str):
            """
            Удаляем текущий профиль и перерисовывает элементы в combo box
            :param json_file: исходный json файл настроек
            :param dt_name: имя диалекта, для которого удаляем профиль
            :return: None
            """
            curr_profile = profile_value_cmbb.currentText()

            # Удаляем профиль из json файла
            del_profile_from_json(json_file, dt_name, curr_profile)

            # Перерисовываем значения для combo box
            init_start_profile_values(json_file, dt_name)


        """ Записываем значения профилей в profile_value_cmbb """
        # Запускаем init_start_profile_values
        init_start_profile_values(PATH_TO_PROFILE_SETTINGS_JSON, dialect_name)








        """ Устанавливаем обработку действий """
        # При изменении активированного профиля
        profile_value_cmbb.activated[str].connect(partial(change_profile,
                                                          PATH_TO_PROFILE_SETTINGS_JSON,
                                                          dialect_name))

        # При нажатии на кнопку добавить, показываем окно заполнени параметров нового профиля
        add_profile_btn.clicked.connect(partial(show_create_new_prof_window,
                                                PATH_TO_PROFILE_SETTINGS_JSON,
                                                dialect_name,
                                                init_start_profile_values))

        # При нажатии удаления текущего профиля
        delete_profile_btn.clicked.connect(partial(del_curr_profile,
                                                   PATH_TO_PROFILE_SETTINGS_JSON,
                                                   dialect_name))
