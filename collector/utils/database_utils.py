from database import inserir_dados
import pandas as pd
import numpy as np

def atualizar_db(df,db,tabela):
    if len(df) == len(db):
        print('Registros Atualizado')
    else:
        df_dif = df.loc[~df['id'].isin(db['id'])].copy()
        inserir_dados(tabela, df_dif)

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
        chaves_para_atualizar = df_dif[['id_season', 'id_competition']]
        df_para_atualizar = df.merge(chaves_para_atualizar, on=chave_conflito, how='inner')
    
        # Aqui você pode chamar sua função de update ou fazer UPSERT
        inserir_dados(tabela, df_para_atualizar, chave_conflito=', '.join(chave_conflito))
        print(f"{len(df_para_atualizar)} registros atualizados.")
   
    

