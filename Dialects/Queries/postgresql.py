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
    conn_string = get_full_con_str(connect_param)

    cnct = psycopg2.connect(conn_string)

    cursor = cnct.cursor()
    sql_query = """
            SELECT d.datname as name
             --, d.datcollate as collation
             --, d.datname as current_object_id
             --, current_schema() as default_schema
            FROM pg_database d
            WHERE 
              d.datistemplate = false
            ORDER BY d.datname
        """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_obj = []

    for i in records:
        out_obj.append(i[0])

    return out_obj


def load_schemes(connect_param: dict = None, db_name: str = None):
    conn_string = get_full_con_str(connect_param)
    cnct = psycopg2.connect(conn_string)

    cursor = cnct.cursor()
    sql_query = """
                select 
                     schema_name as name
                  from information_schema.schemata
                where
                 catalog_name = '{}'
                order by schema_name;
            """.format(db_name)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def load_tables(connect_param: dict = None, db_name: str = None, schema_name: str = None):
    conn_string = get_full_con_str(connect_param)
    cnct = psycopg2.connect(conn_string)

    cursor = cnct.cursor()
    sql_query = """
            select
             t.table_name as name
            from 
             information_schema.tables t
            where 
             t.table_type = 'BASE TABLE'
             --AND t.table_catalog = '' 
             AND t.table_schema = '{}' 
            order by
             t.table_name;
        """.format(schema_name)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr
