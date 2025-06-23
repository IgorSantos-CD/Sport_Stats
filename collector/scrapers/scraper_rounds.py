from selenium_local import iniciar_driver
from database import executar_query
from selenium.webdriver.common.by import By
from utils import transformar_json, gerar_dataframe, delay_aleatorio
from tqdm import tqdm

def coletar_rodadas():
    seasons = executar_query('SELECT id, id_competition FROM seasons', fetch='all')
    driver = iniciar_driver()

    rounds = []
    for _, row in seasons.iterrows():
        id_season = row['id']
        id_comp = row['id_competition']

        driver.get(f"https://www.sofascore.com/api/v1/unique-tournament/{id_comp}/season/{id_season}/rounds")
        delay_aleatorio(1.5,3.0)
        pre = driver.find_element(By.TAG_NAME, 'pre').text
        json_rounds = transformar_json(pre)

            