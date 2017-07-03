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
    # conn_string = get_full_con_str(connect_param)
    psycopg2.connect(**connect_param)

    # Если не будет ошибки вернем True, обработка ошибок в вызове этой функции
    return True
    # return sys.exc_info()[1].args[0]

def load_databases(connect_param: dict = None):
    pass


def load_schemes(connect_param: dict = None, db_name: str = None):
    # conn_string = get_full_con_str(connect_param)
    cnct = psycopg2.connect(**connect_param)

    cursor = cnct.cursor()
    sql_query = """
                select 
                n.nspname as name
              from pg_namespace n;
            """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def load_tables(connect_param: dict = None, db_name: str = None, schema_name: str = None):
    # conn_string = get_full_con_str(connect_param)
    cnct = psycopg2.connect(**connect_param)

    cursor = cnct.cursor()
    sql_query = """
            SELECT  
           c.relname AS name
           FROM 
             pg_namespace nc
             inner join pg_class c on c.relnamespace = nc.oid
             inner join  pg_user u on u.usesysid = c.relowner
             left join pg_catalog.pg_attribute a  ON c.oid = a.attrelid  and a.attisdistkey = 1
           WHERE 
             c.relkind = 'r'
           AND nc.nspname = '{}';
        """.format(schema_name)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr
