from scrapers.scraper_matches import coletar_partidas_temporada_lote, coletar_partidas_temporada
from scrapers.scraper_stats import coletar_match_stats_selenium
from utils.date_utils import format_stat_name, map_period_to_half
from selenium_local.automation import iniciar_driver
from database.db_connection import conectar_banco
from database.db_actions import inserir_dados, select_dados
import pandas as pd
import time


if __name__ == "__main__":

    start = time.time()
    
    # COLETAR PARTIDAS DAS TEMPORADAS
    #base = pd.read_csv(r"C:\Users\VIPEXGRUNT182\Desktop\Igor\Vs Code\Pessoal\Sport_Stats\output\Seasons.csv")

    #df = coletar_partidas_temporada_lote(base)

    #df.to_csv('./output/partidas_temporada.csv', index=False)

    conn = conectar_banco()

    data = select_dados(conn, 'matches', ['id','home_team_id','away_team_id'], fetch='one')
    
    match_id = data[0]
    home_team_id = data[1]
    away_team_id = data[2]

    df_stats = coletar_match_stats_selenium(match_id, home_team_id, away_team_id)

    print(df_stats.head())

    '''if df_stats is not None:
        df_stats.to_csv('./output/stats_game.csv')
    else:
        print("Nenhuma estatística coletada.")'''

    
    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")