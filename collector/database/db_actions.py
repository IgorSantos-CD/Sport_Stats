import pandas as pd
import psycopg2
from psycopg2 import sql


def inserir_dados(tabela, dataframe, conn):
    cursor = conn.cursor()

    colunas = list(dataframe.columns)
    valores = [tuple(x) for x in dataframe.to_numpy()]

    insert_query = sql.SQL(
        "INSERT INTO {tabela} ({campos}) VALUES ({placeholders})"
    ).format(
        tabela = sql.Identifier(tabela),
        campos = sql.SQL(', ').join(map(sql.Identifier, colunas)),
        placeholders = sql.SQL(', ').join(sql.Placeholder()*len(colunas))
    )

    try:
        cursor.executemany(insert_query.as_string(conn), valores)
        conn.commit()
        print(f"Dados inseridos na tabela {tabela}")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir na tabela {tabela}: {e}")
    finally:
        cursor.close()

def select_dados(conn, tabela, colunas=['*'], fetch="all"):
    cursor = conn.cursor()

    if len(colunas) == 1 and colunas[0] == "*":
        cols = "*"
    else:
        cols = ", ".join(colunas)

    querie = f"SELECT {cols} FROM {tabela} WHERE id_competition = 325"

    cursor.execute(querie)
    
    if fetch == "all":
        data = cursor.fetchall()
    elif fetch == "many":
        data = cursor.fetchmany()
    elif fetch == "one":
        data = cursor.fetchone()

    cursor.close()

    return data