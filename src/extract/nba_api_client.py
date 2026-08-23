import time
import logging
import pandas as pd
from nba_api.stats.endpoints import commonteamroster, playercareerstats

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def buscar_elenco(team_id: int) -> pd.DataFrame:
    elenco = commonteamroster.CommonTeamRoster(team_id=team_id)
    return elenco.get_data_frames()[0]

def buscar_carreira_jogador(player_id: int, tentativas_maximas: int = 3) -> pd.DataFrame | None:
    tentativas = 0
    while tentativas < tentativas_maximas:
        try:
            carreira = playercareerstats.PlayerCareerStats(player_id=player_id, timeout=60)
            return carreira.get_data_frames()[0]
        except Exception as erro:
            tentativas += 1
            logger.warning(f"Tentativa {tentativas} falhou para jogador {player_id}: {erro}")
            time.sleep(3)
    logger.error(f"Todas as {tentativas_maximas} tentativas falharam para o jogador {player_id}")        
    return None

def buscar_estatisticas_time(team_id: int) -> tuple[pd.DataFrame, list]:
    df_elenco = buscar_elenco(team_id)
    lista_estatisticas = []
    falhas = []

    for _, jogador in df_elenco.iterrows():
        df_carreira = buscar_carreira_jogador(jogador["PLAYER_ID"])
        if df_carreira is not None:
            lista_estatisticas.append(df_carreira)
        else:
            falhas.append(jogador["PLAYER"])
        time.sleep(1.0)
    df_final = pd.concat(lista_estatisticas, ignore_index=True)
    return df_final, falhas    