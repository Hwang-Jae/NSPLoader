import pyodbc
import pandas as pd
import clickhouse_connect

from config import (
    SQL_CONFIG,
    CLICKHOUSE_CONFIG,
    TABLES
)

# SQL Server 연결
sql_conn = pyodbc.connect(
    f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={SQL_CONFIG['server']};
    DATABASE={SQL_CONFIG['database']};
    UID={SQL_CONFIG['username']};
    PWD={SQL_CONFIG['password']};
    """
)

# ClickHouse 연결
ch_client = clickhouse_connect.get_client(
    host=CLICKHOUSE_CONFIG["host"],
    port=CLICKHOUSE_CONFIG["port"],
    username=CLICKHOUSE_CONFIG["username"],
    password=CLICKHOUSE_CONFIG["password"],
    database=CLICKHOUSE_CONFIG["database"]
)


def create_clickhouse_table(df, target_table):

    columns = []

    for col in df.columns:

        dtype = str(df[col].dtype)

        if "int" in dtype:
            ch_type = "Int64"

        elif "float" in dtype:
            ch_type = "Float64"

        elif "datetime" in dtype:
            ch_type = "DateTime"

        else:
            ch_type = "String"

        columns.append(
            f"`{col}` {ch_type}"
        )

    ddl = f"""
    CREATE TABLE IF NOT EXISTS {target_table}
    (
        {','.join(columns)}
    )
    ENGINE = MergeTree()
    ORDER BY tuple()
    """

    ch_client.command(ddl)


def sync_table(source_table, target_table):

    print(
        f"[START] {source_table}"
    )

    sql = f"""
    SELECT *
    FROM {source_table}
    """

    df = pd.read_sql(
        sql,
        sql_conn
    )

    print(
        f"Rows : {len(df)}"
    )

    if len(df) == 0:
        return

    create_clickhouse_table(
        df,
        target_table
    )

    ch_client.command(
        f"TRUNCATE TABLE {target_table}"
    )

    ch_client.insert_df(
        target_table,
        df
    )

    print(
        f"[SUCCESS] {target_table}"
    )


def run():

    for table in TABLES:

        sync_table(
            table["source_table"],
            table["target_table"]
        )


if __name__ == "__main__":
    run()