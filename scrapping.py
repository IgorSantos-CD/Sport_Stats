import pandas as pd
from selenium_local import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep

#INICIALIZANDO O NAVEGADOR E ACESSANDO A PÁGINA PARA SCRAPPING
driver = iniciar_driver()
driver.get("https://www.sofascore.com/api/v1/sport/football/categories/all")

json_categorias = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

dicionario_paises = {}
for item in json_categorias['categories']:
    name = item['name']
    name_id = item['id']
    dicionario_paises[name] = name_id

driver.get("https://www.sofascore.com/api/v1/config/default-unique-tournaments/BR/football")

json_torneios = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

dicionario_torneios = {}
for item in json_torneios['uniqueTournaments']:
    id_torneio = item['id']
    infos = {
        "name" : item['name'],
        "slug" : item['slug'],
        "primary_color" : item.get('primaryColorHex', None),
        "secondary_color" : item.get('secondaryColorHex', None),
        "id_pais" : item['category']['id']
        }
    dicionario_torneios[id_torneio] = infos

dicionario_seasons = {}
for comp_id in dicionario_torneios.keys():
    driver.get(f"https://api.sofascore.com/api/v1/unique-tournament/{comp_id}/seasons")
    json_seasons = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)
    for item in json_seasons['seasons']:
        id_season = item['id']
        data_season = {
            "id_competition" : comp_id,
            "year" : item['year']
            }
        dicionario_seasons[id_season] = data_season