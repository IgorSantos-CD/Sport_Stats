import pandas as pd
from selenium_local import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import json
from time import sleep

#INICIALIZANDO O NAVEGADOR E ACESSANDO A PÁGINA PARA SCRAPPING
driver = iniciar_driver()
driver.get("https://www.sofascore.com/api/v1/sport/football/categories/all")

json_categorias = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

#BUSCANDO PAÍSES VIA API
dicionario_paises = {}
for item in json_categorias['categories']:
    name = item['name']
    name_id = item['id']
    dicionario_paises[name] = name_id

driver.get("https://www.sofascore.com/api/v1/config/default-unique-tournaments/BR/football")

js= json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)

#BUSCANDO TORNEIOS VIA API
dicionario_torneios = {}
for item in js['uniqueTournaments']:
    id_torneio = item['id']
    infos = {
        "name" : item['name'],
        "slug" : item['slug'],
        "primary_color" : item.get('primaryColorHex', None),
        "secondary_color" : item.get('secondaryColorHex', None),
        "id_pais" : item['category']['id']
        }
    dicionario_torneios[id_torneio] = infos

#BUSCANDO TEMPORADAS VIA API
dicionario_seasons = {}
for comp_id in dicionario_torneios.keys():
    driver.get(f"https://api.sofascore.com/api/v1/unique-tournament/{comp_id}/seasons")
    js = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)
    for item in js['seasons']:
        id_season = item['id']
        data_season = {
            "id_competition" : comp_id,
            "year" : item['year']
            }
        dicionario_seasons[id_season] = data_season

#BUSCANDO TIMES VIA API
erros = {}
teams = {}
for comp_id in tqdm(dicionario_torneios.keys()):

    filter_dic = {
        id_season : data
        for id_season, data in dicionario_seasons.items()
        if data['id_competition'] == comp_id
    }
    for id_season in tqdm(filter_dic):
        driver.get(f"https://www.sofascore.com/api/v1/unique-tournament/{comp_id}/season/{id_season}/standings/total")
        js = json.loads(driver.find_element(By.XPATH, "/html/body/pre").text)
        try:
            for item in js['standings']:
                teams_season = item['rows']
                try:
                    for team in teams_season:
                        team_info = team['team']
                        id_team = team_info.get('id',0)
                        dados_team = {
                            "id_season" : id_season,
                            "id_comp" : comp_id,
                            "country" : team_info.get('country', 0).get('alpha3', 0),
                            "name" : team_info.get('name',0),
                            "short_name" : team_info.get('short_name', 0),
                            "color_primary" : team_info.get('teamColors',0).get('primary',0),
                            "color_secondary" : team_info.get('teamColors',0).get('secondary',0)
                        }
                        teams[id_team] = dados_team
                except Exception as e:
                    print(f'Erro ao extrair informações do time | {e}')
                    pass
        except Exception as e:
            erros[comp_id] = {id_season : e}

df_teams = pd.DataFrame.from_dict(teams, orient='index')
df_teams.to_csv('./output/Teams.csv')

df_erros = pd.DataFrame.from_dict(erros, orient='index')
df_erros.to_csv('./output/erros.csv')