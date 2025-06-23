import time
from scrapers import coletar_paises, coletar_competicoes,coletar_seasons, coletar_rodadas
from database import executar_query, inserir_dados


if __name__ == "__main__":
    start = time.time()

    '''#COLETANDO PAISES DISPONIVEIS PARA CONSULTA
    df_paises = coletar_paises()
    bd_paises = executar_query('SELECT * FROM countries')
    if len(df_paises) == len(bd_paises):
        print("Registros Atualizados!")
    else:
        df_dif = df_paises.loc[~df_paises['id'].isin(bd_paises['id'])].copy()
        inserir_dados('countries', df_dif)

    #COLETANDO COMPETIÇÕES DISPONÍVEIS PARA CONSULTA
    df_competitions = coletar_competicoes()
    bd_competitions = executar_query('SELECT * FROM competitions', fetch='all')
    if len(df_competitions) == len(bd_competitions):
        print("Registros Atualizados!")
    else:
        df_dif = df_competitions.loc[~df_competitions['id'].isin(bd_competitions['id'])].copy()
        inserir_dados('competitions', df_dif)

    df_seasons = coletar_seasons()
    bd_seasons = executar_query('SELECT * FROM seasons', fetch='all')
    if len(df_seasons) == len(bd_seasons):
        print("Registros Atualizados!")
    else: 
        df_dif = df_seasons.loc[~df_seasons['id'].isin(bd_seasons['id'])].copy()
        inserir_dados('seasons', df_dif)'''
    
    coletar_rodadas()


    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")