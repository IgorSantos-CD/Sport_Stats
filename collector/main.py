import time
from scrapers import coletar_paises, coletar_competicoes,coletar_seasons, coletar_rodadas, coletar_partidas_por_rodada
from database import executar_query, inserir_dados, conectar_banco_nuvem
from utils import atualizar_db, atualizar_registros


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
 
    
    '''df_matches, df_teams = coletar_partidas_por_rodada()

    teams_merge = df_teams.merge(
        right=bd_teams,
        on = 'id',
        how='left',
        suffixes=('_api','_bd')
    )

    matches_merge = df_matches.merge(
        right=bd_matches,
        on='id',
        how='left',
        suffixes=('_api','_bd')
    )
    

    df_dif = teams_merge[
        (teams_merge['name_api'] != teams_merge['name_bd']) |
        (teams_merge['short_name_api'] != teams_merge['short_name_bd']) |
        (teams_merge['primary_color_api'] != teams_merge['primary_color_bd']) |
        (teams_merge['secondary_color_api'] != teams_merge['secondary_color_bd']) |
        (teams_merge['country_alpha_api'] != teams_merge['country_alpha_bd'])
        ]
    chaves_para_atualizar = df_dif['id']
    df_para_atualizar = df_teams.merge(
        right=chaves_para_atualizar,
        on= 'id',
        how='inner'
    )

    if df_dif.empty and len(df_teams) == len(bd_teams):
        print("Registros Atualizados")
    else:
        chaves_para_atualizar = df_dif['id']
        df_para_atualizar = df_teams.merge(
            right=chaves_para_atualizar,
            on= 'id',
            how='inner'
        )

        inserir_dados('teams', df_para_atualizar)
        print(f"{len(df_para_atualizar)} registros atualizados.")
    
    df_dif = matches_merge[
        (matches_merge['date_api'] != matches_merge['date_bd']) |
        (matches_merge['status_api'] != matches_merge['status_bd']) |
        (matches_merge['id_season_api'] != matches_merge['id_season_bd']) |
        (matches_merge['id_competition_api'] != matches_merge['id_competition_bd']) |
        (matches_merge['home_team_id_api'] != matches_merge['home_team_id_bd']) |
        (matches_merge['away_team_id_api'] != matches_merge['away_team_id_bd']) |
        (matches_merge['home_score_api'] != matches_merge['home_score_bd']) |
        (matches_merge['away_score_api'] != matches_merge['away_score_bd']) |
        (matches_merge['winner_api'] != matches_merge['winner_bd']) |
        (matches_merge['round_api'] != matches_merge['round_bd']) |
        (matches_merge['timestamp_api'] != matches_merge['timestamp_bd'])
    ]
    
    if df_dif.empty and len(df_matches) == len(bd_matches):
        print("Registros Atualizados")
    else:
        chaves_para_atualizar = df_dif['id']
        df_para_atualizar = df_matches.merge(
            right=chaves_para_atualizar,
            on= 'id',
            how='inner'
        )

        inserir_dados('matches', df_para_atualizar)
        print(f"{len(df_para_atualizar)} registros atualizados.")'''
    

    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")