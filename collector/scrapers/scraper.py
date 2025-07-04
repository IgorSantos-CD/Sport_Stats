from collector.selenium_local import iniciar_driver
from collector.scrapers import coletar_jogos_do_dia, coletar_jogos_anteriores
from collector.utils import transformar_json
from selenium.webdriver.common.by import By
import pandas as pd
import time

def coleta_por_data():
    data_atual = time.localtime()
    dia = f"{data_atual.tm_mday:02d}"
    mes = f"{data_atual.tm_mon:02d}"
    ano = f"{data_atual.tm_year:04d}"

    driver = iniciar_driver()

    url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{ano}-{mes}-{dia}"
    driver.get(url)

    pre = driver.find_element(By.TAG_NAME,"pre").text
    json_data = transformar_json(pre)

    driver.quit()


    paises, unique_comps, comps, seasons, teams, matches = coletar_jogos_do_dia(json_data)

    last_countries, last_unique_competitions, last_competitions, last_seasons, last_matches, last_teams = coletar_jogos_anteriores(teams)

    df_countries = pd.concat([paises, last_countries], ignore_index=True,).drop_duplicates(subset='id')
    df_unique_competitions = pd.concat([unique_comps, last_unique_competitions], ignore_index=True,).drop_duplicates(subset='id')
    df_competitions = pd.concat([comps, last_competitions], ignore_index=True,).drop_duplicates(subset='slug_name')
    df_seasons = pd.concat([seasons, last_seasons], ignore_index=True).drop_duplicates(subset='id')
    df_teams = pd.concat([teams, last_teams], ignore_index=True).drop_duplicates(subset='id')
    df_matches = pd.concat([matches, last_matches], ignore_index=True).drop_duplicates(subset='id')

    return {
        "countries" : df_countries, 
        "unique_competitions" : df_unique_competitions, 
        "competitions" : df_competitions, 
        "seasons" : df_seasons,
        "teams" : df_teams,
        "matches" : df_matches
    }




