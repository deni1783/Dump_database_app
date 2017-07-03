import psycopg2


""" Обработка ошибок в вызове функций """



def get_full_con_str(obj):
    con_str = ''
    host = obj['host']
    port = obj['port']
    user = obj['user']
    password = obj['password']
    database = obj['database']

    if host != '[default]':
        con_str += "host='{}'".format(host)

    # USER
    con_str += " user='{}'".format(user)

    # PASSWORD
    if password:
        con_str += " password='{}'".format(password)

    if database:
        con_str += " dbname='{}'".format(database)

    return con_str

def check_connect(connect_param: dict = None):
    conn_string = get_full_con_str(connect_param)
    psycopg2.connect(conn_string)

    # Если не будет ошибки вернем True, обработка ошибок в вызове этой функции
    return True
    # return sys.exc_info()[1].args[0]

def load_databases(connect_param: dict = None):
    out_arr = [
        'database1',
        'database2',
        'database3',
        'database4'
    ]
    return out_arr


def load_schemes(connect_param: dict = None, db_name: str = None):
    out_arr = [
        db_name + '_schema1',
        db_name + '_schema2',
        db_name + '_schema3',
        db_name + '_schema4',
        db_name + '_schema5'
    ]
    return out_arr


def load_tables(connect_param: dict = None, db_name: str = None, schema_name: str = None):
    out_arr = [
        schema_name + '_table1',
        schema_name + '_table2',
        schema_name + '_table3',
        schema_name + '_table4',
        schema_name + '_table5',
        schema_name + '_table6'
    ]
    return out_arr
