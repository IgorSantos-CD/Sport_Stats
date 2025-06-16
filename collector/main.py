from scrapers.scraper_matches import coletar_partidas_temporada
import pandas as pd
import time


if __name__ == "__main__":

    start = time.time()
    #Campeonato Brasileiro 2024
    base = pd.read_csv(r"C:\Users\VIPEXGRUNT182\Desktop\Igor\Vs Code\Pessoal\Sport_Stats\output\Seasons.csv")

    df = coletar_partidas_temporada(base)

    df.to_csv('./output/partidas_temporada.csv', index=False)
    
    end = time.time()

    print(f"Tempo de execução: {end-start:.2f} segundos")