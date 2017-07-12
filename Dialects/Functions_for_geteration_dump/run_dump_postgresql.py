from Custom_modules.Functions.easy_fn import wrap_double_quote
from Custom_modules.Functions import json_fn, ui_fn, cmd_fn
from Custom_modules.Constants import PATH_TO_CUSTOM_SETTINGS_JSON
from Dialects.Custom_widgets.custom_postgresql import select_path_to_pgdump

from functools import partial

from PyQt5 import QtCore
# from Modules.my_classes.ClassForCMD.for_cmd import run_cmd
# from Modules.my_classes.custom_functions import write_to_log



class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, list_of_cmd, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.list_cmd = list_of_cmd
        self.cmd = None
        self.code = None
        self.stdout = None
        self.stderr = None
        self.object = None

    def run(self):
        for i in self.list_cmd:
            # self.sleep(2)
            # self.object = i[0]
            # self.cmd = i[1]
            self.cmd = i
            self.mysignal.emit(i)
            # print(self.object)
            # print(self.cmd)
            (self.code, self.stdout, self.stderr) = cmd_fn.run_cmd(self.cmd)
            # write_to_log(self.dialect_name, self.object,
            #              self.stdout, self.code,
            #              self.stderr)
            # self.mysignal.emit(i)









def make_list_cmd_for_bcp(path_to_pg_dump: str, connecting_settings: dict, obj_dict: dict, type_of_dump: str, out_dir: str):
    """
    Функция формирует список готовых строк для запуска дампа

    :param path_to_pg_dump: путь к pg_dump.exe
    :param connecting_settings: параметры подключения
    :param obj_dict: словарь выбранных элементов
    :param type_of_dump:
    :param out_dir: путь к папке назначения
    :return: list
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

    host = ' --host={}'.format(connecting_settings['host'])
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



    prepare_str = wrap_double_quote(path_to_pg_dump) + host + port + user + type_d


    all_cmd = []
    # ' --host=VM-DBA-2008R2-5 --port=5432 --username=qa -a -tDBCS_D_AZURE_DW approximatenumerics -tDBCS_D_AZURE_DW characterstrings "DBCS_D_AZURE_DW"'

    for db_name in obj_dict:

        schema = {}
        # Заполняем объект
        # schema: {
        #   table_name1: [' -t ""schema"."table"']
        #   table_name2: [' -t ""schema"."table"']
        # }
        for schema_name in obj_dict[db_name]:
            schema[schema_name] = []
            for table_name in obj_dict[db_name][schema_name]:

                # Оборачиваем схему и таблицу в отдельные двойные кавычки
                schema[schema_name].append(' -t' + r'"\"{}\".\"{}\""'.format(schema_name, table_name))


        # selected_tables_bd = ''

        # Проходим и генерируем полную строку
        for s in schema:
            selected_tables_bd = ' --file="{}"'.format(out_dir + '/' + db_name + '--' + s + '.sql')
            for t in schema[s]:
                selected_tables_bd += t
            selected_tables_bd += ' "{}"'.format(db_name)
            """
            prepare_str + selected_tables_bd =             
                [
                '"C:/Program Files/PostgreSQL/9.5/bin/pg_dump.exe" --host=VM-DBA-2008R2-5 --port=5432 --username=qa -a --file=D://DBCS_BIG_TABLES -t"\\"DBCS_BIG_TABLES\\".\\"all_types_redshift_10t\\" -t"\\"DBCS_BIG_TABLES\\".\\"all_types_redshift_1m_add\\" "DBCS_BIG_TABLES"', 
                '"C:/Program Files/PostgreSQL/9.5/bin/pg_dump.exe" --host=VM-DBA-2008R2-5 --port=5432 --username=qa -a --file=D://DBCS_D_AZURE_DW -t"\\"DBCS_D_AZURE_DW\\".\\"approximatenumerics\\" -t"\\"DBCS_D_AZURE_DW\\".\\"characterstrings\\" "DBCS_D_AZURE_DW"'
                 ]
            """
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


    def on_started_thread():
        log_area.append('DUMP generation started')

    def on_change_thread(s):
        print(s)
        log_area.append(s)

    def on_finished_thread():
        log_area.append('DUMP generation finished')
        parent_obj.run_dump_btn.setDisabled(False)
        ui_fn.change_cursor('normal')


    # Проверяем что указан путь к pg_dump.exe
    json_data = json_fn.get_full_json_data(PATH_TO_CUSTOM_SETTINGS_JSON)
    if 'postgresql' not in json_data or 'path_to_pgdump' not in json_data['postgresql']:
        path_to_pgdump = select_path_to_pgdump(PATH_TO_CUSTOM_SETTINGS_JSON)
        if not path_to_pgdump:
            ui_fn.show_error_msg_window('pg_dump.exe not found!', 'Please select path to pg_dump.exe', parent_obj)
    else:
        path_to_pgdump = json_data['postgresql']['path_to_pgdump']

    # Заполняем список подготовленными командами
    all_cmd_commands = make_list_cmd_for_bcp(path_to_pgdump, curr_conn_settings,
                                             selected_objects_dict, selected_type_of_dump,
                                             out_put_dir)
    # print(all_cmd_commands)
    # for s in all_cmd_commands:
    #     (return_code, stdout, stderr) = cmd_fn.run_cmd(s)
    #
    #     # Если произошла ошибка в ходе виполнения выводим окно ошибки
    #     if return_code:
    #         raise NameError(stderr)

    mythread = MyThread(all_cmd_commands)
    mythread.started.connect(on_started_thread)
    mythread.mysignal.connect(on_change_thread, QtCore.Qt.QueuedConnection)
    mythread.finished.connect(on_finished_thread)

    mythread.start()


