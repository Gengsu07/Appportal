from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

mysql_username = os.getenv("LOCAL_MYSQL_USERNAME")
mysql_password = os.getenv("LOCAL_MYSQL_PASSWORD")
mysql_host = os.getenv("LOCAL_MYSQL_HOST")
mysql_con = create_engine(
    f"mysql://{mysql_username}:{mysql_password}@{mysql_host}/mpninfo"
)

postgres_username = os.getenv("POSTGRES_USERNAME")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_password_parse = quote_plus(postgres_password)
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database = os.getenv("POSTGRES_DB")
postgre_con = create_engine(
    f"postgresql://{postgres_username}:{postgres_password_parse}@{postgres_host}/{postgres_database}"
)


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
    index: object = False,
):
    df.to_sql(sql_table, con=mysql_con, index=index, if_exists="replace")

    print(f"LOAD TO MYSQL {sql_table}:OK")


if __name__ == "__main__":
    print(postgres_password)
    # print(postgres_password_parse)
