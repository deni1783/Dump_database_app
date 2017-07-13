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
            SELECT datname FROM pg_catalog.pg_database
            where datname not in 
            ( 'postgres'
            , 'template0'
            , 'template1'
            , 'gpadmin'
            , 'gpperfmon'
            ) order by 1;
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
                SELECT
                  sm.nspname AS name 
                FROM
                  pg_namespace sm
            """

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
            SELECT
          t.relname AS name
        FROM
          pg_class t
          JOIN gp_distribution_policy gdp
            ON t.oid = gdp.localoid
          JOIN pg_namespace ns
            ON ns.oid = t.relnamespace
        WHERE
          t.relkind = 'r'
          AND t.relstorage <> 'x'
          AND NOT EXISTS (SELECT 1 FROM pg_partitions prt WHERE prt.partitiontablename = t.relname AND prt.partitionschemaname = ns.nspname)
          AND ns.nspname = '{}' 
        """.format(schema_name)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr
