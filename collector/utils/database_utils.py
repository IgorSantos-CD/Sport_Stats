from database import inserir_dados, executar_query
import pandas as pd
import numpy as np

def atualizar_db(df,tabela):
    if df.empty:
        print(f"[AVISO] DataFrame vazio - nada a inserir na tabela '{tabela}'.")
        return

    # Verifica se a coluna 'id' existe no DataFrame
    if 'id' in df.columns:
        # Busca os IDs já existentes no banco
        query = f"SELECT id FROM {tabela};"
        db_ids = executar_query(query, fetch='all')

        if db_ids.empty:
            df_dif = df
        else:
            df_dif = df[~df['id'].isin(db_ids['id'])]

        if df_dif.empty:
            print(f"[INFO] Nenhum novo registro para inserir na tabela '{tabela}'.")
        else:
            inserir_dados(tabela, df_dif)
            print(f"[OK] {len(df_dif)} novos registros inseridos na tabela '{tabela}'.")
    else:
        # Caso não tenha coluna 'id', insere todos os registros
        inserir_dados(tabela, df)
        print(f"[OK] {len(df)} registros inseridos na tabela '{tabela}' (sem controle de ID).")

def atualizar_registros(df,db,tabela,chave_conflito):
    if isinstance(chave_conflito,str):
        chave_conflito = [chave_conflito]
    
    colunas_mutaveis = [col for col in df.columns if col not in chave_conflito]
    
    df_merged = df.merge(
        db,
        on = chave_conflito,
        how = 'left',
        suffixes=('_api','_bd')
    )

    condicoes_diferenca = [
        df_merged[f'{col}_api'] != df_merged[f'{col}_bd']
        for col in colunas_mutaveis
        if f'{col}_bd' in df_merged.columns  # Garante que a coluna existe no df_merged
    ]

    # Combina todas as condições usando o operador de OU
    if condicoes_diferenca:
        df_dif = df_merged.loc[
            np.logical_or.reduce(condicoes_diferenca)
        ]
    else:
        df_dif = pd.DataFrame(columns=df.columns)

    if df_dif.empty and len(df) == len(db):
        print("Registros Atualizados")
    else:
        # Filtra os dados do df_rounds que precisam ser atualizados
        chaves_para_atualizar = df_dif[chave_conflito]
        df_para_atualizar = df.merge(chaves_para_atualizar, on=chave_conflito, how='inner')
    
        # Aqui você pode chamar sua função de update ou fazer UPSERT
        inserir_dados(tabela, df_para_atualizar, chave_conflito=', '.join(chave_conflito))
        print(f"{len(df_para_atualizar)} registros atualizados.")

def buscar_partidas_para_coletar_stats():
    query = """
        SELECT id, home_team_id, away_team_id
        FROM matches
        WHERE status = 'Ended';    
    """
    return executar_query(query, fetch='all')
   
    

