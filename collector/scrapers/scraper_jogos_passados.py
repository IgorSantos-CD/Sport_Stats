import pandas as pd
from selenium.webdriver.common.by import By
from collector.selenium_local import iniciar_driver
from collector.utils import delay_aleatorio, transformar_json
from tqdm import tqdm

def coletar_jogos_anteriores(df_teams):
    teams = list(df_teams['id'])
    unique_competitions = []
    competitions = []
    countries = []
    seasons = []
    teams_last = []
    matches = []

    driver = iniciar_driver()

    for team in tqdm(teams):
        url = f"https://www.sofascore.com/api/v1/team/{team}/events/last/0"
        driver.get(url)
        delay_aleatorio(0.5,1.2)

        pre = driver.find_element(By.TAG_NAME,"pre").text
        lista_10_ultimos_jogos = transformar_json(pre)['events'][::-1][:11]

        for p in lista_10_ultimos_jogos:
            country_data = p.get('tournament', {}).get('uniqueTournament',{}).get('category', {})
            tournament_data = p.get('tournament', {})
            unique_tournament_data = p.get('tournament',{}).get('uniqueTournament',{})
            season_data = p.get('season', {})
            home_team_data = p.get('homeTeam', {})
            away_team_data = p.get('awayTeam', {})

            country = {
                'id' : country_data.get('id', 0) if country_data else tournament_data.get('category', {}).get('id',0),
                'name' : country_data.get('name') if country_data else tournament_data.get('category', {}).get('name',0),
                'slug_name' : country_data.get('slug') if country_data else tournament_data.get('category', {}).get('slug'),
                'priority' : unique_tournament_data.get('priority',0) if unique_tournament_data else tournament_data.get('priority',0),
                'flag' : country_data.get('flag') if country_data else tournament_data.get('category', {}).get('flag')
            }

            competition = {
                'name' : tournament_data.get('name'),
                'slug_name' : tournament_data.get('slug'),
                'unique_comp_id' : unique_tournament_data.get('id', 0) if unique_tournament_data else tournament_data.get('id',0)
            }

            unique_competition = {
                'id' : unique_tournament_data.get('id', 0) if unique_tournament_data else tournament_data.get('id',0),
                'name' : unique_tournament_data.get('name') if unique_tournament_data else tournament_data.get('name'),
                'slug_name' : unique_tournament_data.get('slug') if unique_tournament_data else tournament_data.get('slug'),
                'location_name' : country_data.get('name') if unique_tournament_data else tournament_data.get('category', {}).get('country', {}).get('name'),
                'location_id' : country_data.get('id', 0) if unique_tournament_data else tournament_data.get('category', {}).get('id',0),
                'location_flag' : country_data.get('flag') if unique_tournament_data else tournament_data.get('category', {}).get('flag'),
                'sport_name' : country_data.get('sport', {}).get('name') if unique_tournament_data else tournament_data.get('category', {}).get('sport', {}).get('name')
            }

            season = {
                'id' : season_data.get('id', 0),
                'name' : season_data.get('name',0),
                'id_competition' : unique_tournament_data.get('id', 0) if unique_tournament_data else tournament_data.get('id',0),
                'year' : season_data.get('year',0),
                'editor' : season_data.get('editor',False)
            }

            home_team = {
                'id' : home_team_data.get('id', 0),
                'name' : home_team_data.get('name'),
                'short_name' : home_team_data.get('shortName'),
                'primary_color' : home_team_data.get('teamColors', {}).get('primary'),
                'secondary_color' : home_team_data.get('teamColors', {}).get('secondary'),
                'country_alpha' : home_team_data.get('country', {}).get('alpha3')
            }


            away_team = {
                'id' : away_team_data.get('id', 0),
                'name' : away_team_data.get('name'),
                'short_name' : away_team_data.get('shortName'),
                'primary_color' : away_team_data.get('teamColors', {}).get('primary'),
                'secondary_color' : away_team_data.get('teamColors', {}).get('secondary'),
                'country_alpha' : away_team_data.get('country', {}).get('alpha3')
            }

            match_info = {
                'id' : p.get('id', 0),
                'date' : pd.to_datetime(p.get('startTimestamp',0), unit='s'),
                'status' : p.get('status', {}).get('description'),
                'id_season' : season_data.get('id',0),
                'id_competition' : unique_tournament_data.get('id',0) if unique_tournament_data else tournament_data.get('id',0),
                'home_team_id' : home_team_data.get('id'),
                'away_team_id' : away_team_data.get('id'),
                'home_score_ft': p.get('homeScore',{}).get('normaltime') if p.get('status', {}).get('description') == 'Ended' else -1,
                'away_score_ft' : p.get('awayScore',{}).get('normaltime') if p.get('status', {}).get('description') == 'Ended' else -1,
                'winner' : p.get('winnerCode') if p.get('status', {}).get('description') == 'Ended' else None,
                'round' : p.get('roundInfo', {}).get('round'),
                'timestamp' : p.get('changes', {}).get('changeTimestamp'),
                'home_score_ht' : p.get('homeScore',{}).get('period1') if p.get('status', {}).get('description') == 'Ended' else -1,
                'away_score_ht' : p.get('awayScore',{}).get('period1') if p.get('status', {}).get('description') == 'Ended' else -1
            }

            countries.append(country)
            unique_competitions.append(unique_competition)
            competitions.append(competition)
            seasons.append(season)
            teams_last.append(home_team)
            teams_last.append(away_team)
            matches.append(match_info)
        
    driver.quit()


    df_countries = pd.DataFrame(countries)
    df_countries = df_countries.drop_duplicates(subset='id')

    df_unique_comp = pd.DataFrame(unique_competitions)
    df_unique_comp = df_unique_comp.drop_duplicates(subset='id')

    df_competitions = pd.DataFrame(competitions)
    df_competitions = df_competitions.drop_duplicates(subset='slug_name')   

    df_seasons = pd.DataFrame(seasons)
    df_seasons = df_seasons.drop_duplicates(subset='id')

    df_matches = pd.DataFrame(matches)
    df_matches = df_matches.drop_duplicates(subset='id')

    df_teams = pd.DataFrame(teams_last)
    df_teams = df_teams.drop_duplicates(subset='id')

    return df_countries, df_unique_comp, df_competitions, df_seasons, df_matches, df_teams