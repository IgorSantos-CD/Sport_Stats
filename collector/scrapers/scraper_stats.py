from collector.selenium_local import iniciar_driver
from database import executar_query
from collector.utils import delay_aleatorio,transformar_json, atualizar_db
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
import pandas as pd
import time
    
def coletar_stats_partida():
    #BUSCA TODOS OS JOGOS FINALIZADOS COM OS TIMES
    query = """
        SELECT id, home_team_id, away_team_id
        FROM matches
        WHERE status = 'Ended';
    """

    df_matches = executar_query(query, fetch="all")

    # BUSCA ESTATS JÁ EXISTENTES NO BANCO
    query_stats_existentes = """
        SELECT match_id, team_id, stat_name, half
        FROM match_stats;
    """
    df_existentes = executar_query(query_stats_existentes, fetch="all")
    df_existentes["assinatura"] = (
        df_existentes["match_id"].astype(str) + "-" +
        df_existentes["team_id"].astype(str) + "-" +
        df_existentes["stat_name"] + "-" +
        df_existentes["half"].astype(str)
    )
    assinaturas_existentes = set(df_existentes["assinatura"])

    driver = iniciar_driver()
    for row in tqdm(df_matches.itertuples(index=False), desc="Estatisticas", total=len(df_matches)):
        match_id = row.id
        home_team_id = row.home_team_id
        away_team_id = row.away_team_id

        try:
            url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
            driver.get(url)
            delay_aleatorio(1.5,1.9)

            pre = driver.find_element(By.TAG_NAME, 'pre').text
            json_data = transformar_json(pre)

            stats = json_data, match_id, home_team_id, away_team_id
            if stats:
                df_stats = pd.DataFrame(stats)
                # GERA ASSINATURA PARA REMOVER DUPLICADOS
                df_stats["assinatura"] = (
                    df_stats["match_id"].astype(str) + "-" +
                    df_stats["team_id"].astype(str) + "-" +
                    df_stats["stat_name"] + "-" +
                    df_stats["half"].astype(str)
                )
                df_stats = df_stats[~df_stats["assinatura"].isin(assinaturas_existentes)].copy()
                df_stats.drop(columns=["assinatura"], inplace=True)
                if not df_stats.empty:
                    atualizar_db(df_stats, 'match_stats')
                    print(f"[OK] Match {match_id} - {len(stats)} stats inseridas")
                else:
                    print(f"[SKIP] Match {match_id} - Nenhuma stat nova")
            else:
                print(f"[SEM DADOS] Match {match_id}")
            
            
        except Exception as e:
            print(f"[ERRO] Match {match_id}: {e}")

    driver.quit()


        