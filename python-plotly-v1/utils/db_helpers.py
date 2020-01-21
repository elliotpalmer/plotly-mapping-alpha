
def db_conn_string(db_cred_json):
    """
    Creates the PostgreSQL connection string
    from a config json file
    """
    d = db_cred_json
    engine_string = (
        'postgresql://' + d['PGUSER'] + ':' + d['PGPASSWORD'] +
        '@' + d['PGHOST'] + ":" + d['PGPORT'] + "/" + d['PGDATABASE']
    )
    return(engine_string)

def db_engine(db_cred_json):
    """
    Creates a sqlalchemy engine from a json file
    """
    from sqlalchemy import create_engine
    conn_string = db_conn_string(db_cred_json)
    engine = create_engine(conn_string, paramstyle='format')
    return(engine)

def split_table_name(table_and_schema):
    """
    Split a 'schema.table_name' into parts to use with pd.to_sql
    """
    table_list = table_and_schema.split(".")
    if len(table_list) == 1:
        schema = None
        table = table_list[0]
    else:
        schema = table_list[0]
        table = table_list[1]
    return([schema, table])

def read_query(sqlPath):
    fd = open(sqlPath, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile

def upload_dataframe(df, name, engine, if_exists='replace', index=False):
    """
    Uploads a dataframe to a PostgreSQL database
    """

    # Import Libraries
    import psycopg2
    import io

    # Table name needs to be split into schema
    table_list = split_table_name(name)
    schema = table_list[0]
    table  = table_list[1]

    # Truncates the table
    df.head(0).to_sql(table, engine, schema=schema, if_exists=if_exists, index=index)

    # Because sometimes people put newlines in text cells and postgre throws a FIT :()
    df.replace("\\n", value="", regex = True, inplace = True)
    # Upload Data
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    cur.copy_from(output, name, null="") # null values become ''
    conn.commit()
