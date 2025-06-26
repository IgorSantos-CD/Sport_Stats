from database import conectar_banco
from psycopg2.extras import execute_values

import pandas as pd
import psycopg2
from psycopg2 import sql


def inserir_dados(tabela, dados, chave_conflito='id'):
    conn = conectar_banco()
    cursor = conn.cursor()

    #GERA STRING COM OS NOMES DAS COLUNAS
    colunas = list(dados.columns)
    colunas_str = ",".join(colunas)

    #CRIA UM TUPLO PARA CADA LINHA DO DATAFRAME
    valores = [tuple(x) for x in dados.to_numpy()]

    #GERA SET PARA COLUNAS QUE SERÃO ATUALIZADAS (EXCLUINDO A CHAVE DE CONFLITO)
    colunas_para_update = [col for col in colunas if col != chave_conflito]
    set_update = ", ".join([f"{col} = EXCLUDED.{col}" for col in colunas_para_update])


    query = f"""
    INSERT INTO {tabela} ({colunas_str})
    VALUES %s
    ON CONFLICT ({chave_conflito}) DO UPDATE SET
    {set_update}
    """

    try:
        execute_values(cursor,query,valores)
        conn.commit()
        print("UPSERT concluído com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao inserir os dados:", e)
    finally:
        print("Processo concluído")
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