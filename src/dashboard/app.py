import sys
from datetime import datetime
from pathlib import Path

# Streamlit executa o script de dentro de src/dashboard; sem isto o
# "from src..." não encontra a raiz do repositório (local e no Streamlit Cloud).
RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from src.analytics.consultas import (  # noqa: E402
    METRICAS_PERMITIDAS,
    contagem_por_tabela,
    listar_temporadas,
    top_jogadores,
    total_por_time,
)
from src.load.database import CAMINHO_BANCO  # noqa: E402

ROTULOS = {
    "pontos": "Pontos",
    "rebotes": "Rebotes",
    "assistencias": "Assistências",
    "roubos": "Roubos de bola",
    "bloqueios": "Bloqueios",
}

PIPELINE_DOT = """
digraph {
    rankdir=LR;
    node [shape=box, style=rounded, fontname="Helvetica"];
    api [label="nba_api"];
    extract [label="extract\\nretry + backoff + logs"];
    transform [label="transform\\nlimpeza e tipos"];
    models [label="models\\ndataclass"];
    load [label="load\\nUNIQUE + INSERT OR IGNORE"];
    db [label="SQLite", shape=cylinder];
    api -> extract -> transform -> models -> load -> db;
}
"""


@st.cache_data(show_spinner=False)
def _temporadas() -> list[str]:
    return listar_temporadas(CAMINHO_BANCO)


@st.cache_data(show_spinner=False)
def _top_jogadores(metrica: str, season_id: str, limite: int) -> pd.DataFrame:
    linhas = top_jogadores(metrica, season_id, limite, CAMINHO_BANCO)
    return pd.DataFrame(linhas, columns=["Jogador", ROTULOS[metrica]])


@st.cache_data(show_spinner=False)
def _total_por_time(metrica: str, season_id: str) -> pd.DataFrame:
    linhas = total_por_time(metrica, season_id, CAMINHO_BANCO)
    return pd.DataFrame(linhas, columns=["Time", ROTULOS[metrica]])


@st.cache_data(show_spinner=False)
def _contagens() -> dict[str, int]:
    return contagem_por_tabela(CAMINHO_BANCO)


def main() -> None:
    st.set_page_config(page_title="NBA Data Warehouse", layout="wide")
    st.title("NBA Data Warehouse")
    st.caption(
        "Pipeline ETL em Python (extract, transform, models, load) alimentando "
        "um warehouse SQLite com tabelas dimensão e fato. Os dados abaixo saem "
        "direto desse banco."
    )

    if not Path(CAMINHO_BANCO).exists():
        st.error(f"Banco não encontrado em {CAMINHO_BANCO}. Rode o ETL antes.")
        st.stop()

    temporadas = _temporadas()
    if not temporadas:
        st.warning("O banco existe, mas a tabela fato está vazia.")
        st.stop()

    with st.sidebar:
        st.header("Filtros")
        temporada = st.selectbox("Temporada", temporadas)
        metrica = st.selectbox(
            "Métrica", METRICAS_PERMITIDAS, format_func=lambda m: ROTULOS[m]
        )
        limite = st.slider("Top N jogadores", min_value=5, max_value=25, value=10)

    aba_analises, aba_pipeline = st.tabs(["Análises", "Pipeline"])

    with aba_analises:
        esquerda, direita = st.columns(2)
        with esquerda:
            st.subheader(f"Top {limite} em {ROTULOS[metrica].lower()}")
            df_jogadores = _top_jogadores(metrica, temporada, limite)
            st.bar_chart(df_jogadores, x="Jogador", y=ROTULOS[metrica], horizontal=True)
        with direita:
            st.subheader(f"{ROTULOS[metrica]} por time")
            df_times = _total_por_time(metrica, temporada)
            st.bar_chart(df_times, x="Time", y=ROTULOS[metrica])
        with st.expander("Ver tabela"):
            st.dataframe(df_jogadores, hide_index=True, width="stretch")

    with aba_pipeline:
        st.subheader("Arquitetura")
        st.graphviz_chart(PIPELINE_DOT)

        st.subheader("Estado do warehouse")
        contagens = _contagens()
        colunas = st.columns(len(contagens))
        for coluna, (tabela, total) in zip(colunas, contagens.items()):
            coluna.metric(tabela, f"{total:,}".replace(",", "."))

        modificado = datetime.fromtimestamp(Path(CAMINHO_BANCO).stat().st_mtime)
        st.caption(f"Arquivo do banco modificado em {modificado:%d/%m/%Y %H:%M}")
        st.markdown("[Código-fonte no GitHub](https://github.com/WellitonT)")


main()