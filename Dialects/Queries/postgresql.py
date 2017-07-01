def check_connect(connect_param: dict = None):
    # return True or False
    return True

def load_databases(connect_param: dict = None):
    out_arr = [
        'database1',
        'database2',
        'database3',
        'database4'
    ]
    return out_arr


def load_schemes(connect_param: dict =None, db_name: str = None):
    out_arr = [
        db_name + '_schema1',
        db_name + '_schema2',
        db_name + '_schema3',
        db_name + '_schema4',
        db_name + '_schema5'
    ]
    return out_arr


def load_tables(connect_param: dict =None, db_name: str = None, schema_name: str = None):
    out_arr = [
        schema_name + '_table1',
        schema_name + '_table2',
        schema_name + '_table3',
        schema_name + '_table4',
        schema_name + '_table5',
        schema_name + '_table6'
    ]
    return out_arr
