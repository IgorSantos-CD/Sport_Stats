from analysis.goals_analysis import dataframe_goals

query_gols = """
SELECT
        id_season,
        date,
        home_team_id as team_id,
        home_score as goals_for,
        away_score as goals_against,
        'home' as venue
    FROM matches

    UNION ALL

    SELECT
        id_season,
        date,
        away_team_id as team_id,
        away_score as goals_for,
        home_score as goals_against,
        'away' as venue
    FROM matches;
"""

'''df_matches = dataframe_goals(query=query_gols)

df_gols = df_matches.groupby(['id_season','team_id']).agg(
    jogos = ('team_id','count'),
    media_gols_feitos = ('goals_for', 'mean'),
    media_gols_sofridos = ('goals_against', 'mean'),
).reset_index()

df_gols['media_gols_total'] = df_gols['media_gols_feitos'] + df_gols['media_gols_sofridos']

print(df_gols.loc[df_gols['id_season'] == 48982])'''

df_countries = dataframe_goals("SELECT * FROM countries")

print(df_countries)