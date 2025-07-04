from database import inserir_dados, executar_query, atualizar_registros
import pandas as pd
import numpy as np

def atualizar_db(df,tabela,chave_duplicada):
    if df.empty:
        print(f"[AVISO] DATAFRAME VAZIO - NADA A INSERIR NA TABELA '{tabela}'.")
        return

    query = f"SELECT * FROM {tabela}"
    bd_registros = pd.DataFrame(executar_query(query, fetch='all'))
    
    if bd_registros.empty:
        print(f"[AVISO] SEM REGISTROS NO BANCO DE DADOS PARA A TABELA '{tabela}'")
        inserir_dados(tabela, df)
        return

    #NOVOS REGISTROS
    df_dif = df[~df[chave_duplicada].isin(bd_registros[chave_duplicada])]

    #REGISTROS CANDIDATOS A UPDATE
    df_merged = df.merge(bd_registros,how='inner',on=chave_duplicada,suffixes=("_api","_bd"))

    condicao_total = pd.Series([False] * len(df_merged)) #VERIFICAR ESSE TRECHO
    for col in df.columns:
        if col in chave_duplicada:
            continue
        col_api = f"{col}_api"
        col_bd = f"{col}_bd"
        if col_api in df_merged.columns and col_bd in df_merged.columns:
            #COMPARA OS VALORES LEVANDO EM CONTA NANS
            diferentes = df_merged[col_api].astype(str).fillna('') != df_merged[col_bd].astype(str).fillna('')
            condicao_total |= diferentes
    
    df_update_base = df_merged[condicao_total]
    df_update = df[df[chave_duplicada].isin(df_update_base[chave_duplicada])]

    if not df_dif.empty:
        try:
            inserir_dados(tabela, df_dif)
            print(f"[OK] {len(df_dif)} REGISTROS INSERIDOS EM '{tabela}'.")
        except Exception as e:
            print(f"[ERRO] NÃO FOI POSSIVEL INCLUIR REGISTROS NA TABELA '{tabela}': {e}")
    else:
        print(f"[AVISO] DATAFRAME VAZIO - NADA NOVO A INSERIR NA TABELA '{tabela}'.")

    try:
        if not df_update.empty:
            try:
                atualizar_registros(tabela, df_update,chave_duplicada)
                print(f"[OK] {len(df_update)} ATUALIZADOS NA TABELA {tabela} COM SUCESSO!")
            except Exception as e:
                print(f"[ERRO] NÃO FOI POSSIVEL ATUALIZAR REGISTROS NA TABELA '{tabela}': {e}")
        else:
            print(f"[AVISO] DATAFRAME VAZIO - NADA PARA ATUALIZAR NA TABELA '{tabela}'.")
    except Exception as e:
        print(f"[ERRO] FALHA AO ATUALIZAR REGISTROS NA TABELA '{tabela}': {e}")
   

def buscar_partidas_para_coletar_stats():
    query = """
        SELECT id, home_team_id, away_team_id
        FROM matches
        WHERE status = 'Ended';    
    """
    return executar_query(query, fetch='all')

   
    

