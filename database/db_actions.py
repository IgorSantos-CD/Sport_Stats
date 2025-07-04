from database import conectar_banco
from psycopg2.extras import execute_values

import pandas as pd
import psycopg2
from psycopg2 import sql


def inserir_dados(tabela, dados):
    conn = conectar_banco()
    cursor = conn.cursor()

    #GERA STRING COM OS NOMES DAS COLUNAS
    colunas = list(dados.columns)
    colunas_str = ",".join(colunas)

    #CRIA UM TUPLO PARA CADA LINHA DO DATAFRAME
    valores = [tuple(x) for x in dados.to_numpy()]

    query = f"""
    INSERT INTO {tabela} ({colunas_str})
    VALUES %s
    """

    try:
        execute_values(cursor,query,valores)
        conn.commit()
        print("[OK] Insert concluído com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao inserir os dados:", e)
    finally:
        cursor.close()
        conn.close()

def atualizar_registros(tabela, dados, chave_duplicada):
    if isinstance(chave_duplicada, str):
        chave_duplicada = [chave_duplicada]

    conn = conectar_banco()
    cursor = conn.cursor()

    colunas = list(dados.columns)
    colunas_update = [col for col in colunas if col not in chave_duplicada]

    set_clause = ",".join([f"{col} = %s" for col in colunas_update])
    where_clause = " AND ".join(f"{col} = %s" for col in chave_duplicada)
    query = f"UPDATE {tabela} SET {set_clause} WHERE {where_clause}"

    for _, row in dados.iterrows():
        valores_set = [row[col] for col in colunas_update]
        valores_where = [row[col] for col in chave_duplicada]
        valores = valores_set + valores_where

        try:
            cursor.execute(query,valores)
        except Exception as e:
            print(f"[ERRO] AO ATUALIZAR REGISTRO {valores_where}: {e}")

    conn.commit()
    cursor.close()
    conn.close()



def executar_query(query, fetch='all'):
    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        colunas = [desc[0] for desc in cursor.description]
        
        if fetch == 'all':
            dados = cursor.fetchall()
        elif fetch == 'one':
            dados = cursor.fetchone()
        else:
            dados = cursor.fetchmany()

        df = pd.DataFrame(dados, columns=colunas)
        return df
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()