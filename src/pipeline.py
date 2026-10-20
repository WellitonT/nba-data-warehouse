"""Orquestrador do ETL: extract -> transform -> models -> load."""
import logging
import sys

from src.extract.nba_api_client import buscar_elenco, buscar_estatisticas_time
from src.transform.limpeza import remover_linhas_totais, corrigir_tipos_numericos
from src.models.estatistica_temporada import criar_estatistica_a_partir_da_linha
from src.load.database import criar_banco, inserir_estatisticas

logger = logging.getLogger(__name__)

TEAM_ID_PADRAO = 1610612747  # Los Angeles Lakers


def run_etl(team_id: int = TEAM_ID_PADRAO) -> None:
    logger.info("Extract: time %s", team_id)
    df_elenco = buscar_elenco(team_id)
    df_carreira, falhas = buscar_estatisticas_time(team_id)
    logger.info(
        "Extract: %d jogadores, %d linhas de carreira, %d falhas",
        len(df_elenco), len(df_carreira), len(falhas),
    )
    if falhas:
        logger.warning("Jogadores sem dados: %s", ", ".join(falhas))

    df_limpo = corrigir_tipos_numericos(remover_linhas_totais(df_carreira))
    logger.info("Transform: %d -> %d linhas", len(df_carreira), len(df_limpo))

    ids_sem_dados = set(df_elenco["PLAYER_ID"]) - set(df_limpo["PLAYER_ID"])
    if ids_sem_dados:
        nomes = df_elenco[df_elenco["PLAYER_ID"].isin(ids_sem_dados)]["PLAYER"]
        logger.info("Sem estatísticas na NBA: %s", ", ".join(nomes))

    estatisticas = [
        criar_estatistica_a_partir_da_linha(linha)
        for _, linha in df_limpo.iterrows()
    ]
    logger.info("Models: %d objetos criados", len(estatisticas))

    criar_banco()
    inserir_estatisticas(estatisticas, df_elenco)
    logger.info("Load: concluído")


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        run_etl()
    except Exception:
        logger.exception("ETL falhou")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())