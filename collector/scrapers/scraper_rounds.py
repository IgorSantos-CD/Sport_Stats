from selenium_local import iniciar_driver
from database import executar_query
from selenium.webdriver.common.by import By
from utils import transformar_json, gerar_dataframe, delay_aleatorio, classificar_formato
from tqdm import tqdm

def coletar_rodadas():
    seasons = executar_query('SELECT id, id_competition FROM seasons')
    driver = iniciar_driver()

    rounds = []
    try:
        for row in tqdm(seasons.itertuples(index=False),desc="Temporadas", total=len(seasons)):
            id_season = row.id
            id_comp = row.id_competition

            try:
                driver.get(f"https://www.sofascore.com/api/v1/unique-tournament/{id_comp}/season/{id_season}/rounds")
                delay_aleatorio(1.5,1.7)
                pre = driver.find_element(By.TAG_NAME, 'pre').text
                json_rounds = transformar_json(pre)
                current_round = json_rounds.get('currentRound', {}).get('round',None)
                rounds_dict = json_rounds.get('rounds',{})
                total_rounds = [r.get('round', '') for r in rounds_dict if 'round' in r]
                last_round_number = total_rounds[-1]
                formato_torneio = classificar_formato(json_rounds['rounds'])
                round_info = {
                    'id_season' : int(id_season),
                    'id_competition' : int(id_comp),
                    'current_round_number' : current_round,
                    'last_round_number' : last_round_number,
                    'type' : formato_torneio,
                    'finished' : True if current_round == last_round_number else False,
                    'total_rounds' : total_rounds
                }

                rounds.append(round_info)
            except Exception as e:
                print(f"Erro ao coletar rodadas da season {id_season} competição {id_comp} | {e}")
    finally:
        driver.quit()

    df = gerar_dataframe(rounds, colunas=['id_season', 'id_competition', 'current_round_number', 'last_round_number', 'type', 'finished', 'total_rounds'])
        
    return df

            