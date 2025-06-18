from selenium_local.automation import iniciar_driver
from utils.date_utils import format_stat_name, map_period_to_half
import json
import pandas as pd
import time

def coletar_match_stats_selenium(match_id, home_team_id, away_team_id):

    driver = iniciar_driver()
    url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"

    try:
        driver.get(url)
        #time.sleep(0.5)

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