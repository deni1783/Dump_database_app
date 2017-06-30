import json

""" для DialectListBox """

def get_dialects_from_json(json_file: str):
    """
    Парсит json-файл со списком диалектов и возвращает полученые диалекты
    Ищет по слючу: sup_dialects_list_data

    :param json_file: путь к файлу
    :return: массив диалектов
    """
    dialects = []
    data = open(json_file).read()
    json_data = json.loads(data)

    for dt_name in json_data['sup_dialects_list_data']:
        dialects.append(dt_name)

    return dialects



""" Работа с профилями настроек подключения """

def get_profile_settings_value(json_file: str, dialect_name: str, profile_name: str):
    """
    Возвращает объект настроек для указанного диалекта -> и профиля для него
    :param json_file: путь к файлу параметров профилей подключения
    :param dialect_name: имя диалекта для которого ищем профиль
    :param profile_name: имя профиля для которого ищем параметры
    :return: dict (со всеми знаяеними)
    """
    data = open(json_file).read()
    json_data = json.loads(data)
    return json_data[dialect_name][profile_name]


def get_all_profiles(json_file: str, dialect_name: str):
    """
    Функция для первоначального заполнения списка доступных профилей
    :param json_file: путь к файлу параметров профилей подключения
    :param dialect_name:  имя диалекта для которого ищем профиль
    :return: list (список профилей)
    """
    data = open(json_file).read()
    json_data = json.loads(data)
    out_arr = []
    for prof_name in json_data[dialect_name]:
        out_arr.append(prof_name)
    return out_arr
