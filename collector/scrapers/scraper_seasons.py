from collector.selenium_local import iniciar_driver
from database import executar_query
from selenium.webdriver.common.by import By
from collector.utils import transformar_json, gerar_dataframe, delay_aleatorio
from tqdm import tqdm

def coletar_seasons():
    driver = iniciar_driver()
    competicoes = executar_query('SELECT id FROM competitions', fetch='all')['id']
    seasons = []
    try:
        for comp in tqdm(competicoes):
            driver.get(f"https://api.sofascore.com/api/v1/unique-tournament/{comp}/seasons")
            delay_aleatorio(1.5,2.0)
            pre = driver.find_element(By.TAG_NAME, 'pre').text
            json_seasons = transformar_json(pre)
        
            for season in json_seasons['seasons']:
                info = {
                    'id' : season.get('id', None),
                    'name' : season.get('name', None),
                    'id_competition' : comp,
                    'year' : season.get('year',1700),
                    'editor' : str(season.get('editor', 'false')).lower() == 'true' 
                }
                seasons.append(info)
    except Exception as e:
        print(f"Não foi possivel coletar informações da competição: {comp}\n")
        print(pre)
        driver.quit()

    driver.quit()
    df = gerar_dataframe(seasons, colunas=['id', 'name', 'year', 'editor', 'id_competition'])

    return df
    