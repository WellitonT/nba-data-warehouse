CREATE TABLE IF NOT EXISTS dim_jogador (
    player_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_time (
    team_id TEXT PRIMARY KEY,
    sigla TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fato_estatisticas_temporada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    season_id TEXT NOT NULL,
    idade REAL,
    jogos_disputados INTEGER,
    minutos INTEGER,
    pontos INTEGER,
    rebotes INTEGER,
    assistencias INTEGER,
    roubos INTEGER,
    bloqueios INTEGER,
    FOREIGN KEY (player_id) REFERENCES dim_jogador(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_time(team_id),
    UNIQUE (player_id, team_id, season_id)
);