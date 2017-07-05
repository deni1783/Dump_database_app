from Custom_modules.Functions.easy_fn import wrap_double_quote

def make_cmd_for_bcp(connecting_settings: dict, obj_list: list, obj_dict: dict, type_of_dump: str):
    """
    Функция формирует готовую строку для запуска дампа
    :param connecting_settings: параметры подключения
    :param obj_list: массив объектов
    :return: str
    """
    """
            default port is 5432


            "%pgdump$cmd%"
            - h % Server$name %
            -U % User$name %
            -p % Port$number %
            -d % Database %
            -n % Scheme$name %
            -t table_name
            % Type %
            -f % dir % % Scheme$name %.sql

            Второй вариант:

            "c:\program files\postgresql\9.5\bin\pg_dump.exe" 
            -h"VM-DBA-2008R2-5" 
            -U"qa" 
            -p5432 
            -s 
            -f"D:\data\from_dump\gp_approxima.sql" 
            -t"\"DBCS_D_GREENPLUM\".approximatenumerics" "DBCS_D_GREENPLUM"
        """

    type_of_dump = type_of_dump.lower()

    host = '--host={}'.format(connecting_settings['host'])
    user = ' --username={}'.format(connecting_settings['user'])

    if connecting_settings['port'] == '[default]':
        port = ' --port={}'.format('5432')
    else:
        port = ' --port={}'.format(connecting_settings['port'])

    if type_of_dump == 'data':
        type_d = ' -a'
    elif type_of_dump == 'schema':
        type_d = ' -s'
    else:
        # type_of_dump == 'full'
        type_d = ''


    prepare_str = host + port + type_d

    all_cmd = []

    for db_name in obj_dict:
        tables = []
        for schema_name in obj_dict[db_name]:
            for table_name in obj_dict[db_name][schema_name]:
                tables.append(' -t' + schema_name + ' ' + table_name)

        selected_tables_bd = ''
        for t in tables:
            selected_tables_bd += t
        selected_tables_bd += ' "{}"'.format(db_name)
        all_cmd.append(prepare_str + selected_tables_bd)


    return all_cmd





def generate_dump(parent_obj,
                  top_level_item_type: str,
                  curr_conn_settings: dict,
                  selected_objects_arr: list,
                  selected_objects_dict: dict,
                  selected_type_of_dump: str,
                  out_put_dir: str,
                  log_area):


    # print(selected_objects_dict)
    print(make_cmd_for_bcp(curr_conn_settings, selected_objects_arr, selected_objects_dict, selected_type_of_dump))