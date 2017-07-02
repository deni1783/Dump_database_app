from PyQt5 import QtWidgets, QtCore
from Custom_modules.Functions import json_fn
from Custom_modules.Constants import PATH_TO_DIALECTS_LIST_JSON


class DialectListBox(QtWidgets.QWidget):
    """
        Класс формирует:
            объект (VBOX) dialects_list_vbox в котором хранятся кнопки для диалектов
            объект (dict) DIALECT_NAME_BTN { имя_диалекта: кнопка }
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Формируем список необходимых диалектов из файла supported_dialects.json
        self.DIALECTS_LIST = json_fn.get_dialects_from_json(PATH_TO_DIALECTS_LIST_JSON)

        # Создаем объект где ключ = имя диалекта, а значение = кнопка
        # Для того, что бы в дальнейшем мы могли ставить обработчики на кнопки
        self.DIALECT_NAME_BTN = {}

        # Создаем вертикальное представление в которое будем добавлять кнопки
        dialects_list_vbox = QtWidgets.QVBoxLayout()
        dialects_list_vbox.setAlignment(QtCore.Qt.AlignTop)

        # Заполняем DIALECT_NAME_BTN и dialects_list_vbox
        for dt_name in self.DIALECTS_LIST:
            self.DIALECT_NAME_BTN[dt_name] = QtWidgets.QPushButton(dt_name)
            dialects_list_vbox.addWidget(self.DIALECT_NAME_BTN[dt_name])



        """ GBOX для приложения """
        self.dialect_list_gbox = QtWidgets.QGroupBox('Dialects')
        self.dialect_list_gbox.setFlat(True)
        self.dialect_list_gbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.dialect_list_gbox.setLayout(dialects_list_vbox)