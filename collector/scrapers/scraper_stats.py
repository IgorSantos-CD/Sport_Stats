from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import json
import pandas as pd
import time

def iniciar_driver(log_level = 3):
    options = Options()
    options.add_argument(f"--log-level={log_level}")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")

    service = Service(executable_path="./webdrivers/msedgedriver.exe")
    driver = webdriver.Edge(options=options, service=service)
    return driver

def coletar_match_stats_selenium(driver, match_id, home_team_id, away_team_id):
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"

    try:
        driver.get(url)
        time.sleep(2)

        pre = driver.find_element("tag name", "pre").text
        data = json.loads(pre)

        registros = []

        try:
            for periodo in data.get('statistics', []):
                period = periodo.get('period')
                half = map_period_to_half(period)

                for group in periodo.get('groups', []):
                    for stat in group.get('statisticsItems', []):
                        stat_name = format_stat_name(stat.get('name'))

                        registros.append({
                            'match_id': match_id,
                            'team_id': home_team_id,
                            'half': half,
                            'stat_name': stat_name,
                            'value': stat.get('home', 0) if stat.get('home') is not None else 0
                        })

                        registros.append({
                            'match_id': match_id,
                            'team_id': away_team_id,
                            'half': half,
                            'stat_name': stat_name,
                            'value': stat.get('away', 0) if stat.get('away') is not None else 0
                        })
        except Exception as e:
            print(f"Erro no parse do match {match_id}: {e}")
            return None

        df = pd.DataFrame(registros)
        return df

    except Exception as e:
        print(f"Erro ao coletar stats do match {match_id}: {e}")
        return None
    
def map_period_to_half(period):
    if period == 'ALL':
        return 0
    elif period == '1ST':
        return 1
    elif period == '2ND':
        return 2
    else:
        return None
    
def format_stat_name(name):
    return name.lower().replace(' ', '_').replace('-', '_')

driver = iniciar_driver()

match_id = 13472733
home_team_id = 2001
away_team_id = 2002

df_stats = coletar_match_stats_selenium(driver, match_id, home_team_id, away_team_id)

if df_stats is not None:
    df_stats.to_csv('./output/stats_game.csv')
else:
    print("Nenhuma estatística coletada.")

driver.quit()