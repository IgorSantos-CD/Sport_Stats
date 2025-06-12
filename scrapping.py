import pandas as pd
from selenium_local import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep

#INICIALIZANDO O NAVEGADOR E ACESSANDO A PÁGINA PARA SCRAPPING
driver = iniciar_driver()
driver.get("https://www.sofascore.com/api/v1/team/1999/team-statistics/seasons")

response = driver.find_element(By.XPATH, "/html/body/pre").text
dicionario = json.loads(response)['uniqueTournamentSeasons']

for item in dicionario:
    seasons = item['seasons']
    for season in seasons:
        liga_nome = season['name']
        liga_id = season['id']
        print(f'{liga_nome} + {liga_id}')

