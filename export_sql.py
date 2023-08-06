from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("sgwi2341")
postgre_con = create_engine(
    "postgresql://postgres:{}@localhost/jaktim".format(password)
)
mysql_con = create_engine("mysql://root@localhost/mpninfo")


def export_postgres(
    df: object,
    sql_table,
    schema: object = "public",
    index: object = False,
) -> object:
    """_summary_

    Args:
        df (_type_): dataframe yg akan diexport
        sql_table (_type_, optional): nama table.
        schema (str, optional): nama schema. Defaults to 'public'.
    """
    df.to_sql(
        sql_table, con=postgre_con, schema=schema, index=index, if_exists="replace"
    )
    print(f"LOAD TO POSTGRES {sql_table}:OK")


def export_mysql(
    df: object,
    sql_table,
    schema: object = "public",
    index: object = False,
):
    df.to_sql(sql_table, con=mysql_con, index=index, if_exists="replace")

    print(f"LOAD TO MYSQL {sql_table}:OK")
