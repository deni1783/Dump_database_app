import json


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
