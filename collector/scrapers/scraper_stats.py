from selenium_local.automation import iniciar_driver
from database.db_connection import conectar_banco
from database.db_actions import inserir_dados
from utils.date_utils import parse_statistics
from utils.scraping_ultis import delay_aleatorio, retry
from tqdm import tqdm
import json
import pandas as pd
import time

def coletar_match_stats_selenium(match_id, home_team_id, away_team_id):

    driver = iniciar_driver()
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"

    try:
        driver.get(url)

        pre = driver.find_element("tag name", "pre").text
        data = json.loads(pre)

        registros = parse_statistics(data, match_id,home_team_id, away_team_id)

        df = pd.DataFrame(registros)
        return df

    except Exception as e:
        print(f"Erro ao coletar stats do match {match_id}: {e}")
        return None


def coletar_stats_em_lote(partidas):
    driver = iniciar_driver()
    todos_registros = []

    for partida in tqdm(partidas):
        match_id = partida[0]
        home_team_id = partida[1]
        away_team_id = partida[2]
        url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
        driver.get(url)
        delay_aleatorio(1.5, 3.5)
        try:
            pre = driver.find_element("tag name", "pre").text
            data = json.loads(pre)
            registros =  parse_statistics(data, match_id, home_team_id, away_team_id)

            if registros:
                todos_registros.extend(registros)
                delay_aleatorio(1.5,3.5)
            else:
                print(f"Match {match_id} sem estatisticas disponíveis")

        except Exception as e:
            print(f"Erro no match {match_id}: {e}")

    driver.quit()

    if todos_registros:
        df = pd.DataFrame(todos_registros)
        df.to_csv('./output/stats_game.csv', index=False)
        print("CSV gerado com sucesso.")
        return df
    else:
        print("Nenhum dado de estatística foi coletado.")
        return pd.DataFrame()  # Retorna DataFrame vazio se nada for coletado


        