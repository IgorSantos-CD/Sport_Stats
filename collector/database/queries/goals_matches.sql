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