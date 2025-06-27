from database import executar_query

query = """
SELECT 
    id_season,
    date,
    home_team_id AS team_id,
    home_score AS goals_for,
    away_score AS goals_against,
    'home' AS venue
FROM matches

UNION ALL

SELECT 
    id_season,
    date,
    away_team_id AS team_id,
    away_score AS goals_for,
    home_score AS goals_against,
    'away' AS venue
FROM matches;
"""

df_matches = executar_query(query)

df_gols = df_matches.groupby(['id_season', 'team_id']).agg(
    jogos=('team_id', 'count'),
    media_gols_feitos=('goals_for', 'mean'),
    media_gols_sofridos=('goals_against', 'mean')
).reset_index()

df_gols['media_gols_total'] = df_gols['media_gols_feitos'] + df_gols['media_gols_sofridos']

print(df_gols.head(5))

