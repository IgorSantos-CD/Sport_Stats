import time
import pandas as pd
from collector.scrapers import coletar_paises, coletar_competicoes,coletar_seasons,coletar_rodadas, coletar_partidas_por_rodada,coletar_stats_partida,coleta_por_data
from collector.utils import buscar_partidas_para_coletar_stats, atualizar_db
from database import executar_query, inserir_dados, conectar_banco_nuvem
#from utils import atualizar_db, atualizar_registros


if __name__ == "__main__":
    start = time.time()


    #COLETANDO INFORMAÇÕES VIA API DE PARTIDAS DO DIA
    dados = coleta_por_data()

    dados['countries'].to_csv('./output/countries_2.csv')
    dados['unique_competitions'].to_csv('./output/unique_competitions_2.csv')
    dados['competitions'].to_csv('./output/competitions_2.csv')
    dados['seasons'].to_csv('./output/seasons_2.csv')
    dados['teams'].to_csv('./output/teams_2.csv')
    dados['matches'].to_csv('./output/matches_2.csv')

    atualizar_db(dados['countries'], "countries",'id')
    atualizar_db(dados['unique_competitions'], "unique_competitions",'id')
    atualizar_db(dados['competitions'], "competitions",'slug_name')
    atualizar_db(dados['seasons'], "seasons",'id')
    atualizar_db(dados['teams'], "teams",'id')
    atualizar_db(dados['matches'], "matches",'id')
 

    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")