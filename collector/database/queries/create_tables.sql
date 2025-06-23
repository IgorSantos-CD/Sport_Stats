-- =====================
-- Tabela Countries
-- =====================
CREATE TABLE countries (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug_name VARCHAR(100),
    priority INT NULL,
    flag VARCHAR(100)
);

-- =====================
-- Tabela Competitions
-- =====================
CREATE TABLE competitions (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    slug_name VARCHAR(150),
    primary_color VARCHAR(10),
    secondary_color VARCHAR(10),
    location_name VARCHAR(100),
    location_id INT REFERENCES countries(id),
    location_flag VARCHAR(100),
    sport_name VARCHAR(100)
);

-- =====================
-- Tabela Seasons
-- =====================
CREATE TABLE seasons (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    id_competition INT REFERENCES competitions(id),
    year VARCHAR(20) NOT NULL,
    editor BOOLEAN,
);

-- =====================
-- Tabela Rodadas
-- =====================
CREATE TABLE rounds (
    id_season BIGINT REFERENCES seasons(id),
    id_competition BIGINT REFERENCES competitions(id),
    current_round_number INTEGER,
    last_round_number INTEGER,
    type VARCHAR(50),
    finished BOOLEAN,
    PRIMARY KEY (id_season, id_competition)
);

-- =====================
-- Tabela Teams
-- =====================
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    id_season INT REFERENCES seasons(id),
    id_competition INT REFERENCES competitions(id),
    country_alpha VARCHAR(5),
    name VARCHAR(150) NOT NULL,
    short_name VARCHAR(50),
    name_slug VARCHAR(150),
    primary_color VARCHAR(10),
    secondary_color VARCHAR(10)
);

-- =====================
-- Tabela Matches
-- =====================
CREATE TABLE matches (
    id BIGINT PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    status VARCHAR(50),
    id_season INT REFERENCES seasons(id),
    id_competition INT REFERENCES competitions(id),
    home_team_id INT REFERENCES teams(id),
    away_team_id INT REFERENCES teams(id),
    home_score INT,
    away_score INT,
    winner VARCHAR(50),
    round VARCHAR(50),
    venue VARCHAR(100),
    timestamp BIGINT
);

-- =====================
-- Tabela MatchStats
-- =====================
CREATE TABLE match_stats (
    id SERIAL PRIMARY KEY,
    match_id BIGINT REFERENCES matches(id),
    team_id INT REFERENCES teams(id),
    half INT CHECK (half IN (0, 1, 2)) DEFAULT 0,
    stat_name VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL
);

-- =====================
-- Índices Recomendados
-- =====================
CREATE INDEX idx_matches_date ON matches(date);
CREATE INDEX idx_matches_competition ON matches(id_competition);
CREATE INDEX idx_matches_teams ON matches(home_team_id, away_team_id);

CREATE INDEX idx_stats_match ON match_stats(match_id);
CREATE INDEX idx_stats_team ON match_stats(team_id);