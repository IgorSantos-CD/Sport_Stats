import pandas as pd
import psycopg2
from psycopg2 import sql

#CONEXÃO COM O BANCO
def conectar_banco():
    conn =psycopg2.connect(
        host = 'localhost',
        database = 'Sport_Stats',
        user = 'postgres',
        password = 'senha123',
        port='5432'
    )
    return conn

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