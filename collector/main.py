import time
from scrapers import coletar_paises, coletar_competicoes,coletar_seasons, coletar_rodadas
from database import executar_query, inserir_dados


if __name__ == "__main__":
    start = time.time()

    #BUSCANDO INFORMAÇÕES NO BANCO DE DADOS
    bd_paises = executar_query('SELECT * FROM countries')
    bd_competitions = executar_query('SELECT * FROM competitions')
    bd_seasons = executar_query('SELECT * FROM seasons')
    bd_rounds = executar_query('SELECT * FROM rounds')
    bd_teams = executar_query('SELECT * FROM teams')
    bd_matches = executar_query('SELECT * FROM matches')
    bd_rounds = executar_query('SELECT * FROM rounds')


    #COLETANDO INFORMAÇÕES VIA API
    df_paises = coletar_paises()
    df_competitions = coletar_competicoes()
    df_seasons = coletar_seasons()
    df_rounds = coletar_rodadas()


    atualizar_db(df_paises, bd_paises, 'countries')
    atualizar_db(df_competitions, bd_competitions,'competitions')
    atualizar_db(df_seasons, bd_seasons, 'seasons')

    atualizar_registros(df_rounds, bd_rounds, 'rounds', ['id_season', 'id_competition'])

    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")