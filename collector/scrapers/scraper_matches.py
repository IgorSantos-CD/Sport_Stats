from selenium_local.automation import iniciar_driver
from database import executar_query
from utils import delay_aleatorio, transformar_json, gerar_dataframe, conversao_segura
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import time
import json


def coletar_partidas_temporada_lote(base):
    """
    Coleta todas as partidas de um lote de temporadas.
    
    Args:
        dataframe: base com as temporadas

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

def coletar_partidas_temporada(id_season, id_competition):
    """
    Função para realizar a coleta de partidas de uma temporada especifica

    #Parâmetros:
        id_season: código da temporada
        id_competition: código da competição 

    #Return
        Dataframe com as informações das partidas
    """

    driver = iniciar_driver()

    url = f"https://www.sofascore.com/api/v1/unique-tournament/{id_competition}/season/{id_season}/team-events/total"

    driver.get(url)

    data = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

    partidas =[]

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
                        'competition_id': id_competition,
                        'venue': evento.get('venue', {}).get('name') if evento.get('venue') else None,
                        'timestamp': evento.get('startTimestamp')
                        }

                        partidas.append(partida)
    except Exception as e:
        print(f"season: {id_season} | competition: {id_competition} | {data}")

    print(partidas[0])


def coletar_partidas_por_rodada():
    query = """
        SELECT id_season, id_competition, total_rounds, current_round_number
        FROM rounds
        WHERE id_competition = 325
    """
    seasons_rodadas = executar_query(query)
    
    partidas = []
    teams = []
    for season in tqdm(seasons_rodadas.itertuples(index=False), total=len(seasons_rodadas), desc="Temporadas"):
        driver = iniciar_driver()
        id_season = season.id_season
        id_competition = season.id_competition
        rounds_list = season.total_rounds
        current_round_number = season.current_round_number
        print(current_round_number)
        for r in tqdm(rounds_list, desc=f"Season {id_season} - Rodadas", leave=False):
            if r <= current_round_number:
                try:
                    url = f"https://www.sofascore.com/api/v1/unique-tournament/{id_competition}/season/{id_season}/events/round/{r}"
                    driver.get(url)
                    pre = driver.find_element(By.TAG_NAME, 'pre').text
                    data = transformar_json(pre)

                    if not data.get('events'):
                        continue

                    for evento in data['events']:
                        partida = {
                            'id' : evento.get('id'),
                            'date' : pd.to_datetime(evento.get('startTimestamp'), unit='s'),
                            'status' : evento.get('status', {}).get('description'),
                            'id_season' : id_season,
                            'id_competition' : id_competition,
                            'home_team_id' : evento.get('homeTeam',{}).get('id'),
                            'away_team_id' : evento.get('awayTeam', {}).get('id'),
                            'home_score' : conversao_segura(evento.get('homeScore', {}).get('current', -1)),
                            'away_score' : conversao_segura(evento.get('awayScore', {}).get('current', -1)),
                            'winner' : conversao_segura(evento.get('winnerCode', -1)),
                            'round' : r,
                            'timestamp' : evento.get('startTimestamp')
                        }

                        home_team ={
                            'id' : evento.get('homeTeam',{}).get('id'),
                            'name' : evento.get('homeTeam', {}).get('name'),
                            'short_name' : evento.get('homeTeam', {}).get('shortName'),
                            'primary_color' : evento.get('homeTeam', {}).get('teamColors', {}).get('primary'),
                            'secondary_color' : evento.get('homeTeam', {}).get('teamColors', {}).get('secondary'),
                            'country_alpha' : evento.get('homeTeam', {}).get('country', {}).get('alpha3')
                        }

                        away_team = {
                            'id' : evento.get('awayTeam',{}).get('id'),
                            'name' : evento.get('awayTeam', {}).get('name'),
                            'short_name' : evento.get('awayTeam', {}).get('shortName'),
                            'primary_color' : evento.get('awayTeam', {}).get('teamColors', {}).get('primary'),
                            'secondary_color' : evento.get('awayTeam', {}).get('teamColors', {}).get('secondary'),
                            'country_alpha' : evento.get('awayTeam', {}).get('country', {}).get('alpha3')
                        }

                        partidas.append(partida)
                        teams.append(home_team)
                        teams.append(away_team)
        
                except Exception as e:
                    print(f"Erro na season {id_season}, rodada {r}: {e}")
        print(f'Partidas da rodada {r} coletadas com sucesso')

        driver.quit()    
        if partidas:
                df = gerar_dataframe(partidas, colunas=['id','date','status','id_season','id_competition','home_team_id','away_team_id','home_score', 'away_score', 'winner','round','timestamp'])
                df_teams = gerar_dataframe(teams, colunas=['id','name','short_name','primary_color', 'secondary_color', 'country_alpha'])
                df_teams = df_teams.drop_duplicates(subset='id')
    
    return df, df_teams
