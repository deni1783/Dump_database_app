import json


def get_full_json_data(json_file: str):
    """
    Получить все данные из json файла

    :param json_file:
    :return: dict со всеми даннымы
    """
    full_data = open(json_file).read()
    return json.loads(full_data)


def re_write_json_file(json_file: str, new_json_data: dict):
    """
     Полностью перезаписывает файл json

    :param json_file: файл который необходимо перезаписать
    :param new_json_data: новый объект, который записываетм
    :return: None
    """
    json.dump(new_json_data, open(json_file, 'w'), indent=2)


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


def write_new_profile_to_json(json_file: str, dialect_name: str, obj_to_write: dict):
    """
     Функция добавляет новый профиль в json файл
    :param json_file: исходный файл json
    :param dialect_name: имя диалекта, для которого добавляем профиль
    :param obj_to_write: объект-содержимое значений для нового профиля
    :return: None
    """
    json_data = get_full_json_data(json_file)

    # Создаем новый объект для профиля
    json_data[dialect_name][obj_to_write['new_profile_name']] = {}

    # Если значения для порта не указано, вставляем '[default]'
    if not obj_to_write['port']:
        obj_to_write['port'] = '[default]'

    # Записываем параметры для нового объкта профиля в объект json_data
    for key in obj_to_write:
        # Пропускаем ключ с название профиля
        if key == 'new_profile_name': continue

        json_data[dialect_name][obj_to_write['new_profile_name']][key] = obj_to_write[key]

    # Записываем новый объект с данными в json_file
    re_write_json_file(json_file, json_data)


def del_profile_from_json(json_file: str, dialect_name: str, profile_name: str):
    """
    Функция удаляет из json файла переданный профиль

    :param json_file: исходный файл json
    :param dialect_name: имя диалекта, для которого удаляем профиль
    :param profile_name: имя профиля, кототрый удаляем
    :return: None
    """
    # Получаем текущие данные из json файла
    old_json = get_full_json_data(json_file)

    # Удаляем необходимый профиль
    del old_json[dialect_name][profile_name]

    # Перезаписываем исходный файл новыми данными
    re_write_json_file(json_file, old_json)


def add_or_change_default_objects(json_file: str, top_lvl_item_type: str, dialect_name: str, profile_name: str, objects_list: list):




    # Преобразуем массив в нормализированные объект
    normalize_objects = {}

    if top_lvl_item_type == 'database':
        # database.schema.table
        for i in objects_list:
            split_str = i.split('.')
            db = split_str[0]
            schema = split_str[1]
            table = split_str[2]

            # Если такой БД еще не было
            if db not in normalize_objects:
                normalize_objects[db] = {}

            # Если такой СХЕМЫ еще не было
            if schema not in normalize_objects[db]:
                normalize_objects[db][schema] = []

            # Добавляем таблицы
            normalize_objects[db][schema].append(table)

    elif top_lvl_item_type == 'schema':
        # schema.table
        for i in objects_list:
            split_str = i.split('.')
            schema = split_str[0]
            table = split_str[1]

            # Если такой СХЕМЫ еще не было
            if schema not in normalize_objects:
                normalize_objects[schema] = []

            # Добавляем таблицы
            normalize_objects[schema].append(table)

    json_data = get_full_json_data(json_file)


    # Если нужно создаем объекты
    if dialect_name not in json_data:
        json_data[dialect_name] = {}
    if profile_name not in json_data[dialect_name]:
        json_data[dialect_name][profile_name] = {}


    # Записываем или перезаписываем данные
    json_data[dialect_name][profile_name] = normalize_objects
    re_write_json_file(json_file, json_data)
