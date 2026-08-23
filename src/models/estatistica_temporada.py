from dataclasses import dataclass

@dataclass
class EstatisticaTemporada:
    player_id: str
    season_id: str
    team_id: str
    team_abbreviation: str
    idade: float
    jogos_disputados: int
    minutos: int
    pontos: int
    rebotes: int
    assistencias: int
    roubos: int
    bloqueios: int

def criar_estatistica_a_partir_da_linha(linha):
    return EstatisticaTemporada(
        player_id=linha["PLAYER_ID"],
        season_id=linha["SEASON_ID"],
        team_id=linha["TEAM_ID"],
        team_abbreviation=linha["TEAM_ABBREVIATION"],
        idade=linha["PLAYER_AGE"],
        jogos_disputados=linha["GP"],
        minutos=linha["MIN"],
        pontos=linha["PTS"],
        rebotes=linha["REB"],
        assistencias=linha["AST"],
        roubos=linha["STL"],
        bloqueios=linha["BLK"]
    )
