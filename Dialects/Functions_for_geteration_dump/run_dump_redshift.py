from Custom_modules.Functions.easy_fn import wrap_double_quote

def prepare_cmd(connecting_settings: dict, obj_list: list):
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



def generate_dump(parent_obj,
                  top_level_item_type: str,
                  curr_conn_settings: dict,
                  selected_objects_arr: list,
                  selected_objects_dict: dict,
                  selected_type_of_dump: str,
                  out_put_dir: str,
                  log_area):

    print(curr_conn_settings)
    print('gen')
    print(out_put_dir)

    print(selected_objects_dict)
