from PyQt5 import QtWidgets
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
        dialects_list = json_fn.get_dialects_from_json(PATH_TO_DIALECTS_LIST_JSON)

        # Создаем объект где ключ = имя диалекта, а значение = кнопка
        # Для того, что бы в дальнейшем мы могли ставить обработчики на кнопки
        self.DIALECT_NAME_BTN = {}

        # Создаем вертикальное представление в которое будем добавлять кнопки
        self.dialects_list_vbox = QtWidgets.QVBoxLayout()

        # Заполняем DIALECT_NAME_BTN и dialects_list_vbox
        for dt_name in dialects_list:
            self.DIALECT_NAME_BTN[dt_name] = QtWidgets.QPushButton(dt_name)
            self.dialects_list_vbox.addWidget(self.DIALECT_NAME_BTN[dt_name])
