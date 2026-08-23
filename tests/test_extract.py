from unittest.mock import patch
import pandas as pd
from src.extract.nba_api_client import buscar_carreira_jogador

def test_buscar_carreira_jogador_sucesso():
    dados_falsos = pd.DataFrame({
        "SEASON_ID": ["2023-24"],
        "PTS": [1500],
    })

    with patch("src.extract.nba_api_client.playercareerstats.PlayerCareerStats") as mock_api:
        mock_api.return_value.get_data_frames.return_value = [dados_falsos]

        resultado = buscar_carreira_jogador(player_id=2544)

        assert resultado is not None
        assert resultado.equals(dados_falsos)