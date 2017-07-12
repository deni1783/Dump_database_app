from PyQt5 import QtWidgets
from functools import partial
from Custom_modules.Functions import json_fn
from Custom_modules.Constants import PATH_TO_CUSTOM_SETTINGS_JSON


def select_path_to_pgdump(path_to_json: str):
    """
    функция показывает окно для выбора файла pg_dump.exe и записывает значене в PATH_TO_CUSTOM_SETTINGS_JSON
    :param path_to_json: путь к файлу для уникальных настроек
    :return: path_to_pgdump: str
    """

    json_data = json_fn.get_full_json_data(path_to_json)

    # Ели ранее уже выбиралься путь,
    # то при открытии окна выбора файла, открываем ранее указанный путь
    # иначе домашнюю директорию
    if 'path_to_pgdump' in json_data:
        start_dir = json_data['path_to_pgdump']
    else:
        start_dir = '/home'

    path_to_pgdump = QtWidgets.QFileDialog.getOpenFileName(caption='Choose pg_dump.exe file',
                                                           directory=start_dir, filter='pg_dump.exe')[0]
    if not path_to_pgdump:
        return

    # Записываем или перезаписываем путь к файлу
    json_data['path_to_pgdump'] = path_to_pgdump

    # Записываем новые данные в файл JSON
    json_fn.re_write_json_file(path_to_json, json_data)
    return path_to_pgdump


def add_custom_settings(main_parent, parent_vbox_object):
    """

    :param main_parent: родитель всего приложения
    :param parent_vbox_object: VBOX, в который добавлюем кастомные виджеты
    :return:
    """

    """" Кнопка выбора пути к pg_dump.exe """
    path_to_pgdump_btn = QtWidgets.QPushButton('Select path to pg_dump.exe')


    """ Обработка событий """
    path_to_pgdump_btn.clicked.connect(partial(select_path_to_pgdump,
                                               PATH_TO_CUSTOM_SETTINGS_JSON))

    # Добавляем выджеты в приложение
    parent_vbox_object.addWidget(path_to_pgdump_btn)
