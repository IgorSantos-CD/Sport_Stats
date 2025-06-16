from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import time
import json

def iniciar_driver(log_level = 3):
    options = Options()
    options.add_argument(f"--log-level={log_level}")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")

    service = Service(executable_path="./webdrivers/msedgedriver.exe")
    driver = webdriver.Edge(options=options, service=service)
    return driver


def coletar_partidas_temporada(base):
    """
    Coleta todas as partidas de uma competição e temporada específica.
    
    Args:
        id_competicao (int): ID da competição (ex: 325)
        id_season (int): ID da temporada (ex: 72034)

    Returns:
        DataFrame: Dados das partidas
    """
    driver = iniciar_driver()

    partidas_total = []

    for row in tqdm(base.itertuples(index=False)):
        id_season = row.id_season
        id_competicao = row.id_competition

        url = f"https://www.sofascore.com/api/v1/unique-tournament/{id_competicao}/season/{id_season}/team-events/total"

        driver.get(url)

        time.sleep(2)  # Tempo para garantir que o carregamento ocorra

        data = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

        try:
            for initial_key, nested_dict1 in data.items():
                for firts_key, nested_dict2 in nested_dict1.items():
                    for second_key, lists in nested_dict2.items():
                        for evento in lists:
                            partida = {
                            'match_id': evento.get('id'),
                            'date': pd.to_datetime(evento.get('startTimestamp'), unit='s'),
                            'home_team_id': evento.get('homeTeam', {}).get('id'),
                            'away_team_id': evento.get('awayTeam', {}).get('id'),
                            'home_team_name': evento.get('homeTeam', {}).get('name'),
                            'away_team_name': evento.get('awayTeam', {}).get('name'),
                            'home_score': evento.get('homeScore', {}).get('current'),
                            'away_score': evento.get('awayScore', {}).get('current'),
                            'status': evento.get('status', {}).get('description'),
                            'winner_code': evento.get('winnerCode'),  # 1: casa, 2: fora, 0: empate, None: não finalizado
                            'round': evento.get('roundInfo', {}).get('round'),
                            'season_id': id_season,
                            'competition_id': id_competicao,
                            'venue': evento.get('venue', {}).get('name') if evento.get('venue') else None,
                            'timestamp': evento.get('startTimestamp')
                            }

                            partidas_total.append(partida)
        except Exception as e:
            print(f"season: {id_season} | competition: {id_competicao} | {data}")
            

    driver.quit()

    df_partidas = pd.DataFrame(partidas_total)

    return df_partidas