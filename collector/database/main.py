from db_connection import conectar_banco, inserir_dados
import pandas as pd

conn = conectar_banco()

#df_countries = pd.read_csv("./output/Paises.csv", sep=";")
#df_competitions = pd.read_csv("./output/Torneios.csv", sep=";")
#df_seasons = pd.read_csv("./output/Seasons.csv", sep=",")
#df_teams = pd.read_csv("./output/Teams.csv", sep=",")
df_matches = pd.read_csv("./output/partidas_temporada.csv", sep=";")
df_matches = df_matches.drop_duplicates(subset='id')

#inserir_dados('countries', df_countries, conn)
#inserir_dados('competitions', df_competitions, conn)
#inserir_dados('seasons', df_seasons, conn)
#inserir_dados('teams', df_teams, conn)
#inserir_dados('matches', df_matches, conn)

conn.close()
print("🚀 Processo finalizado.")