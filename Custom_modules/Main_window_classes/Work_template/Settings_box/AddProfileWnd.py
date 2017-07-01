from PyQt5 import QtWidgets, QtCore


class AddingNewProfileWindow(QtWidgets.QWidget):
    def __init__(self, parent, path_to_json: str):
        QtWidgets.QWidget.__init__(self, parent)

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

        """ Параметры подключения (GRID) """
        connecting_string_grid = QtWidgets.QGridLayout()
        connecting_string_grid.setAlignment(QtCore.Qt.AlignTop)



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


        self.create_profile_wnd = QtWidgets.QWidget(parent)
        self.create_profile_wnd.setWindowFlags(QtCore.Qt.Tool)
        self.create_profile_wnd.setWindowTitle('New profile')

        self.create_profile_wnd.setLayout(connecting_string_grid)
        # self.setLayout(connecting_string_grid)
        # create_profile_wnd.show()
