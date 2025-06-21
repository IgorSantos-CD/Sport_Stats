#from scrapers.scraper_matches import coletar_partidas_temporada_lote, coletar_partidas_temporada
from scrapers.scraper_stats import coletar_match_stats_selenium, coletar_stats_em_lote
from utils.date_utils import format_stat_name, map_period_to_half, trata_stats
#from selenium_local.automation import iniciar_driver
from database.db_connection import conectar_banco
from database.db_actions import inserir_dados, select_dados
import pandas as pd
import time


if __name__ == "__main__":

    start = time.time()
    conn = conectar_banco()

    data = select_dados(conn, 'matches', ['id', 'home_team_id', 'away_team_id'])

    conn.close()

    df = coletar_stats_em_lote(data)

    df_tratado = trata_stats(df)

    conn = conectar_banco()

    inserir_dados("match_stats",df_tratado, conn)

    conn.close()

    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")